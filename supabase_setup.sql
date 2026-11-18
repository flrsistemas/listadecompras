-- =====================================================================
--  LISTA DE COMPRAS COMPARTILHADA — Setup do Supabase
--  Cole este script inteiro em: Supabase > SQL Editor > New query > Run
--  É seguro rodar mais de uma vez (idempotente).
-- =====================================================================

-- ---------- TABELAS ---------------------------------------------------

create table if not exists public.profiles (
  id    uuid primary key references auth.users(id) on delete cascade,
  email text not null unique,
  nome  text
);

create table if not exists public.shopping_lists (
  id         uuid primary key default gen_random_uuid(),
  name       text not null check (char_length(name) between 1 and 80),
  owner_id   uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists public.list_members (
  list_id  uuid not null references public.shopping_lists(id) on delete cascade,
  user_id  uuid not null references public.profiles(id) on delete cascade,
  added_at timestamptz not null default now(),
  primary key (list_id, user_id)
);

create table if not exists public.shopping_items (
  id         uuid primary key default gen_random_uuid(),
  list_id    uuid not null references public.shopping_lists(id) on delete cascade,
  name       text not null check (char_length(name) between 1 and 120),
  quantity   text,
  category   text not null default 'Outros',
  is_checked boolean not null default false,
  created_by uuid default auth.uid() references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now()
);

-- Preço do item (opcional); a soma por lista é feita no app
alter table public.shopping_items add column if not exists price numeric(10,2) check (price is null or price >= 0);

create index if not exists idx_items_list   on public.shopping_items(list_id);
create index if not exists idx_members_user on public.list_members(user_id);

-- ---------- TRIGGERS --------------------------------------------------

-- Cria o perfil automaticamente quando um usuário se cadastra
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, nome)
  values (
    new.id,
    lower(new.email),
    coalesce(nullif(new.raw_user_meta_data->>'nome', ''), split_part(new.email, '@', 1))
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Perfis para usuários que já existiam antes deste script
insert into public.profiles (id, email, nome)
select u.id, lower(u.email), split_part(u.email, '@', 1)
from auth.users u
on conflict (id) do nothing;

-- O dono da lista vira membro automaticamente
create or replace function public.add_owner_as_member()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.list_members (list_id, user_id)
  values (new.id, new.owner_id)
  on conflict do nothing;
  return new;
end;
$$;

drop trigger if exists on_list_created on public.shopping_lists;
create trigger on_list_created
  after insert on public.shopping_lists
  for each row execute function public.add_owner_as_member();

-- Atualiza updated_at nos itens
create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists items_touch on public.shopping_items;
create trigger items_touch
  before update on public.shopping_items
  for each row execute function public.touch_updated_at();

-- ---------- FUNÇÕES AUXILIARES (evitam recursão nas políticas RLS) -----

create or replace function public.is_list_owner(p_list uuid)
returns boolean
language sql
stable
security definer set search_path = public
as $$
  select exists (
    select 1 from public.shopping_lists
    where id = p_list and owner_id = auth.uid()
  );
$$;

create or replace function public.is_list_member(p_list uuid)
returns boolean
language sql
stable
security definer set search_path = public
as $$
  select exists (
    select 1 from public.list_members
    where list_id = p_list and user_id = auth.uid()
  ) or exists (
    select 1 from public.shopping_lists
    where id = p_list and owner_id = auth.uid()
  );
$$;

-- Compartilhar lista por e-mail (somente o dono)
create or replace function public.share_list(p_list_id uuid, p_email text)
returns void
language plpgsql
security definer set search_path = public
as $$
declare
  v_user uuid;
begin
  if not public.is_list_owner(p_list_id) then
    raise exception 'Somente o dono da lista pode compartilhá-la';
  end if;

  select id into v_user from public.profiles where email = lower(trim(p_email));
  if v_user is null then
    raise exception 'Nenhum usuário cadastrado com este e-mail';
  end if;

  insert into public.list_members (list_id, user_id)
  values (p_list_id, v_user)
  on conflict do nothing;
end;
$$;

revoke all on function public.share_list(uuid, text) from public, anon;
grant execute on function public.share_list(uuid, text) to authenticated;

-- ---------- RLS -------------------------------------------------------

alter table public.profiles       enable row level security;
alter table public.shopping_lists enable row level security;
alter table public.list_members   enable row level security;
alter table public.shopping_items enable row level security;

-- profiles: vê o próprio perfil e o de quem divide lista com você
drop policy if exists profiles_select on public.profiles;
create policy profiles_select on public.profiles for select to authenticated
using (
  id = auth.uid()
  or exists (
    select 1
    from public.list_members me
    join public.list_members other on other.list_id = me.list_id
    where me.user_id = auth.uid() and other.user_id = profiles.id
  )
);

drop policy if exists profiles_update on public.profiles;
create policy profiles_update on public.profiles for update to authenticated
using (id = auth.uid()) with check (id = auth.uid());

-- shopping_lists
drop policy if exists lists_select on public.shopping_lists;
create policy lists_select on public.shopping_lists for select to authenticated
using (owner_id = auth.uid() or public.is_list_member(id));

drop policy if exists lists_insert on public.shopping_lists;
create policy lists_insert on public.shopping_lists for insert to authenticated
with check (owner_id = auth.uid());

drop policy if exists lists_update on public.shopping_lists;
create policy lists_update on public.shopping_lists for update to authenticated
using (owner_id = auth.uid()) with check (owner_id = auth.uid());

drop policy if exists lists_delete on public.shopping_lists;
create policy lists_delete on public.shopping_lists for delete to authenticated
using (owner_id = auth.uid());

-- list_members
drop policy if exists members_select on public.list_members;
create policy members_select on public.list_members for select to authenticated
using (user_id = auth.uid() or public.is_list_member(list_id));

drop policy if exists members_insert on public.list_members;
create policy members_insert on public.list_members for insert to authenticated
with check (public.is_list_owner(list_id));

drop policy if exists members_delete on public.list_members;
create policy members_delete on public.list_members for delete to authenticated
using (
  public.is_list_owner(list_id)                 -- dono remove qualquer um
  or (user_id = auth.uid())                     -- membro pode sair da lista
);

-- shopping_items
drop policy if exists items_select on public.shopping_items;
create policy items_select on public.shopping_items for select to authenticated
using (public.is_list_member(list_id));

drop policy if exists items_insert on public.shopping_items;
create policy items_insert on public.shopping_items for insert to authenticated
with check (public.is_list_member(list_id));

drop policy if exists items_update on public.shopping_items;
create policy items_update on public.shopping_items for update to authenticated
using (public.is_list_member(list_id)) with check (public.is_list_member(list_id));

drop policy if exists items_delete on public.shopping_items;
create policy items_delete on public.shopping_items for delete to authenticated
using (public.is_list_member(list_id));

-- ---------- ENDURECIMENTO DE FUNÇÕES ----------------------------------
alter function public.touch_updated_at() set search_path = public;
revoke execute on function public.handle_new_user() from public, anon, authenticated;
revoke execute on function public.add_owner_as_member() from public, anon, authenticated;
revoke execute on function public.is_list_owner(uuid) from public, anon;
revoke execute on function public.is_list_member(uuid) from public, anon;
grant execute on function public.is_list_owner(uuid) to authenticated;
grant execute on function public.is_list_member(uuid) to authenticated;

-- ---------- REALTIME --------------------------------------------------

-- DELETE precisa carregar list_id para o cliente filtrar o evento
alter table public.shopping_items replica identity full;

do $$
declare t text;
begin
  foreach t in array array['shopping_items', 'list_members'] loop
    if not exists (
      select 1 from pg_publication_tables
      where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = t
    ) then
      execute format('alter publication supabase_realtime add table public.%I', t);
    end if;
  end loop;
end $$;

-- ---------- PERMISSÕES ------------------------------------------------
grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on all tables in schema public to authenticated;
grant select on public.profiles to anon;  -- usado só pelo keep-alive (RLS devolve vazio)
