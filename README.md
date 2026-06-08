# Sistema de Recomendação Automotivo (Amazon Reviews 2023)

Este projeto implementa um sistema de recomendação de produtos e peças automotivas, baseado no dataset público de avaliações da Amazon (versão 2023, mantido pelo laboratório do Professor Julian McAuley).

O sistema foi desenvolvido como uma API utilizando o **FastAPI** e é totalmente containerizado com **Docker**, atendendo aos seguintes requisitos:
1. Recomendação baseada em um conjunto de dados real (Amazon Automotive).
2. Modelo desenvolvido em Python (com Pandas e Scikit-learn).
3. API FastAPI contendo endpoints para adicionar usuários, itens, preferências e consultar recomendações.
4. Containerização com Docker e Docker Compose.
5. Testes automatizados e documentação.

## Aluno:
- Nome: Raul Falluh Fragoso de Mendonça
- Matrícula: 22300926
- Instituição: Centro Universitário de Brasília
- Curso: Ciência da Computação
- Período: 7º Semestre
- Matéria: Desenvolvimento de sistemas de IA
- Professor: Fábio Oliveira Guimarães 

## Como Funciona

O projeto extrai uma amostra de reviews de usuários que compraram produtos da categoria `Automotive`. A partir do histórico de notas (ratings de 1 a 5 estrelas) de diferentes itens, o modelo de Filtragem Colaborativa é capaz de identificar similaridades e sugerir novas peças e acessórios que possam interessar a um determinado usuário.

## Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados na máquina.

### Passos para Execução
1. Clone este repositório e navegue até a pasta do projeto.
2. Construa a imagem e inicie os contêineres:
   ```bash
   docker-compose up --build
   ```
3. Acesse a documentação interativa da API (Swagger UI) pelo navegador em:
   `http://localhost:8000/docs`

## Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Framework Web:** FastAPI, Uvicorn
- **Data Science / ML:** Pandas, Numpy, Scikit-learn, Datasets (Hugging Face)
- **Infraestrutura:** Docker, Docker Compose
- **Testes:** Pytest, Httpx

## Endpoints da API
A API provê as seguintes rotas principais:
- `POST /users/` - Adicionar novo usuário.
- `POST /items/` - Adicionar um novo item automotivo.
- `POST /ratings/` - Atualizar as preferências (notas) de um usuário sobre um item.
- `GET /recommendations/{user_id}` - Retornar a lista de itens automotivos recomendados.

---
*Projeto desenvolvido para a disciplina Desenvolvimento de sistemas de IA.*
