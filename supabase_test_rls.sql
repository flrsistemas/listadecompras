-- =====================================================================
--  TESTE DE RLS — Lista de Compras
--  Cole em: Supabase > SQL Editor > New query > Run
--
--  Cria 3 usuários e 1 lista de teste, exercita o RLS e termina com um
--  erro PROPOSITAL ("RESULTADO_TESTE ...") que desfaz TUDO (rollback).
--  Nenhum dado fica gravado. O resultado aparece na mensagem do erro.
-- =====================================================================
do $$
declare
  a uuid := gen_random_uuid(); b uuid := gen_random_uuid(); c uuid := gen_random_uuid();
  l uuid; n int; res text := '';
begin
  insert into auth.users (id, email, aud, role) values
    (a,'teste_a@example.test','authenticated','authenticated'),
    (b,'teste_b@example.test','authenticated','authenticated'),
    (c,'teste_c@example.test','authenticated','authenticated');
  res := res || 'perfis criados (esperado 3): ' || (select count(*) from public.profiles where id in (a,b,c)) || E'\n';

  -- A cria lista e item
  perform set_config('request.jwt.claims', json_build_object('sub',a,'role','authenticated')::text, true);
  set local role authenticated;
  insert into public.shopping_lists(name) values ('Lista teste') returning id into l;
  insert into public.shopping_items(list_id,name) values (l,'Leite');
  select count(*) into n from public.list_members where list_id=l;
  res := res || 'A dono virou membro (esperado 1): ' || n || E'\n';

  -- C (não membro) não vê nem altera nada
  reset role;
  perform set_config('request.jwt.claims', json_build_object('sub',c,'role','authenticated')::text, true);
  set local role authenticated;
  select count(*) into n from public.shopping_lists; res := res || 'C ve listas (esperado 0): ' || n || E'\n';
  select count(*) into n from public.shopping_items; res := res || 'C ve itens (esperado 0): ' || n || E'\n';
  begin
    insert into public.shopping_items(list_id,name) values (l,'Intruso');
    res := res || 'C inseriu item: FALHA DE SEGURANCA' || E'\n';
  exception when others then res := res || 'C insert bloqueado: ok' || E'\n'; end;
  begin
    perform public.share_list(l,'teste_c@example.test');
    res := res || 'C share_list: FALHA DE SEGURANCA' || E'\n';
  exception when others then res := res || 'C share_list bloqueado: ok (' || sqlerrm || ')' || E'\n'; end;

  -- A compartilha com B
  reset role;
  perform set_config('request.jwt.claims', json_build_object('sub',a,'role','authenticated')::text, true);
  set local role authenticated;
  perform public.share_list(l,'teste_b@example.test');

  -- B agora vê e edita, mas não apaga a lista de A
  reset role;
  perform set_config('request.jwt.claims', json_build_object('sub',b,'role','authenticated')::text, true);
  set local role authenticated;
  select count(*) into n from public.shopping_items; res := res || 'B ve itens apos share (esperado 1): ' || n || E'\n';
  update public.shopping_items set is_checked=true where list_id=l; get diagnostics n = row_count;
  res := res || 'B atualizou itens (esperado 1): ' || n || E'\n';
  delete from public.shopping_lists where id=l; get diagnostics n = row_count;
  res := res || 'B apagou lista alheia (esperado 0): ' || n || E'\n';

  -- anon não vê nada
  reset role;
  set local role anon;
  select count(*) into n from public.profiles; res := res || 'anon ve perfis (esperado 0): ' || n || E'\n';

  raise exception E'RESULTADO_TESTE (rollback total):\n%', res;
end $$;
