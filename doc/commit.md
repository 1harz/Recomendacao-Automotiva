# Histórico e Fila de Commits

Para dar aspecto de um projeto de alta complexidade e longo prazo, a implementação foi dividida em passos granulares. Marque com `[x]` à medida que for subindo os commits no seu terminal.

## Fase 1: Setup e Dados
- [x] docs(readme): adicionando documentacao inicial do projeto sobre sistema de recomendacao automotivo (Resolves #1)
- [x] feat(data): adicionando amostra de 50k linhas do dataset amazon automotive em formato csv (Resolves #2)
- [x] chore(etl): adicionando script de reducao de dataset e documentacao do fluxo (Resolves #34)
- [x] chore(env): configuracao inicial do ambiente virtual e requirements.txt (Resolves #3)
- [x] chore(git): configuracao de regras de exclusao no .gitignore (Resolves #4)

## Fase 2: Estrutura Base da API (FastAPI)
- [x] feat(api): criacao do esqueleto da aplicacao FastAPI em src/main.py (Resolves #5)
- [x] feat(models): definicao de schemas Pydantic para UserCreate e ItemCreate (Resolves #6)
- [x] feat(models): definicao de schemas Pydantic para RatingCreate e RecommendationResponse (Resolves #7)
- [ ] feat(api): implementacao da rota de boas-vindas (root) e meta-informacoes (Resolves #8)
- [ ] feat(api): implementacao da rota de health check para monitoramento do estado do sistema (Resolves #9)
- [ ] feat(api): criacao do endpoint de cadastro de novos usuarios (POST /users) (Resolves #10)
- [ ] feat(api): criacao do endpoint de inclusao de itens automotivos no catalogo (POST /items) (Resolves #11)
- [ ] feat(api): implementacao de rotas utilitarias para listagem de dados na memoria (GET /items e GET /users) (Resolves #12)
- [ ] docs(readme): atualizando documentacao com endpoints da API e suas funcoes basicas (Resolves #13)

## Fase 3: Motor de Inteligência Artificial (Machine Learning)
- [ ] feat(ml): estrutura da classe RecommenderSystem baseada em OOP em src/recommender.py (Resolves #14)
- [ ] feat(ml): logica de carregamento assincrono de datasets csv com Pandas (Resolves #15)
- [ ] feat(ml): rotina de tratamento de dados esparsos e limpeza inicial de outliers (Resolves #16)
- [ ] feat(ml): implementacao pesada do calculo de Similaridade de Cosseno (Cosine Similarity) (Resolves #17)
- [ ] feat(ml): construcao e fatoracao automatica da matriz usuario-item (Resolves #18)
- [ ] feat(ml): logica de atualizacao dinamica da matriz ao receber novas avaliacoes em tempo real (Resolves #19)
- [ ] feat(ml): implementacao da estrategia de Cold Start (itens populares) para atenuar falta de historico (Resolves #20)
- [ ] feat(ml): funcao principal de recomendacao cruzando historico do usuario com similaridade (Resolves #21)
- [ ] docs(readme): atualizando documentacao explicando a heuristica, a matematica da IA e como ela decide os itens (Resolves #22)

## Fase 4: Integração de Sistemas (API + ML)
- [ ] feat(api): integracao do endpoint de avaliacao de produtos (POST /ratings) com o modelo de ML (Resolves #23)
- [ ] feat(api): validacao de regras de negocio restritas para ratings (notas absolutas entre 1.0 e 5.0) (Resolves #24)
- [ ] feat(api): implementacao e roteamento do endpoint final de sugestoes (GET /recommendations) (Resolves #25)
- [ ] docs(api): enriquecimento do Swagger UI com descricao detalhada e instrucoes do algoritmo de IA (Resolves #26)

## Fase 5: Qualidade, Infraestrutura e Testes
- [ ] test: configuracao inicial da suite de testes usando framework pytest (Resolves #27)
- [ ] test(api): adicao de casos de uso rigorosos para endpoints de criacao de usuario e item (Resolves #28)
- [ ] test(api): validacao de cenarios de erro, excecoes HTTP e limites na avaliacao (Resolves #29)
- [ ] test(ml): bateria de testes de integracao verificando consistencia nas respostas de fallback (Cold Start) (Resolves #30)
- [ ] chore(docker): criacao de imagem isolada via Dockerfile otimizando camadas e cache (Resolves #31)
- [ ] chore(docker): criacao do docker-compose.yml mapeando portas, volumes e ambiente de execucao (Resolves #32)
- [ ] docs(readme): atualizacao final do README contendo as instrucoes de uso do Swagger, testes e Docker build (Resolves #33)
