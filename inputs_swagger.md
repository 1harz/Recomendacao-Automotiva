# Guia Rápido de Testes no Swagger

Siga o passo a passo abaixo para testar o fluxo do sistema diretamente pela interface do Swagger (`http://localhost:8000/docs`).

---

### 1. Criar um Usuário: `POST /users/`
1. Expanda a aba **Usuarios**, clique em **POST /users/** e depois em **Try it out**.
2. Cole o código abaixo na caixa do *Request body*:
```json
{
  "user_id": "USUARIO_BANCA",
  "name": "Avaliador do Projeto"
}
```
3. Clique em **Execute**. Você receberá um retorno `200 OK`.

---

### 2. Cadastrar uma Peça Automotiva Nova: `POST /items/`
1. Expanda a aba **Itens**, clique em **POST /items/** e depois em **Try it out**.
2. Cole o código abaixo na caixa do *Request body*:
```json
{
  "parent_asin": "PECA_TESTE_01",
  "title": "Kit Farol de Milha LED Ultra Forte",
  "price": 149.90,
  "average_rating": 5.0
}
```
3. Clique em **Execute**. 

---

### 3. Avaliar a Peça Criada: `POST /ratings/`
1. Expanda a aba **Avaliacoes**, clique em **POST /ratings/** e depois em **Try it out**.
2. Cole o código abaixo na caixa do *Request body*:
```json
{
  "user_id": "USUARIO_BANCA",
  "parent_asin": "PECA_TESTE_01",
  "rating": 5.0
}
```
3. Clique em **Execute**. O banco de dados da Inteligência Artificial registrará essa nova interação.

---

### 4. Obter Recomendações: `GET /recommendations/{user_id}`
1. Expanda a aba **Recomendacoes**, clique no **GET /recommendations/{user_id}** e depois em **Try it out**.
2. Preencha o campo **user_id** com: `USUARIO_BANCA`
3. Deixe o campo **n** com `5`.
4. Clique em **Execute**.

---

### Entendendo os Resultados (Cold Start)

Você notará que o sistema retornou itens variados (como galão de combustível, adesivos, etc.) com `"score": 5`. 

**Por que isso acontece e o que significa?**
Isso é uma demonstração perfeita do sistema de **Cold Start (Início Frio)** em ação!

1. A `PECA_TESTE_01` é uma peça completamente nova.
2. Como nenhum outro usuário do dataset original (Amazon) comprou ou avaliou essa peça, a Inteligência Artificial (Filtragem Colaborativa) não consegue cruzar dados para encontrar "usuários parecidos" com o `USUARIO_BANCA`. A similaridade é zero.
3. Quando isso ocorre, o algoritmo entra em modo de segurança *(fallback)* e passa a recomendar os **itens globais mais populares e mais bem avaliados** de todo o catálogo.

Essa heurística garante que, mesmo sem ter histórico cruzado suficiente, o sistema sempre faça boas recomendações para o cliente final.
