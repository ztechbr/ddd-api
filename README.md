DDD Brasil API (Flask + REST + Swagger + GraphQL)

Endpoints:
- REST:
  - GET /api/ddd/<code>
  - GET /api/ddds?uf=SP&estado=rio&q=texto
  - GET /api/search?q=texto
  - GET /health
- Swagger UI:
  - /apidocs/
- GraphQL (com GraphiQL):
  - /graphql

Rodar local:
  pip install -r requirements.txt
  python app.py

Rodar com Docker:
  docker compose up --build

Exemplos:
  curl http://localhost:5000/api/ddd/21
  curl "http://localhost:5000/api/ddds?uf=SP"
  curl "http://localhost:5000/api/search?q=fortaleza"

Nota:
A lista embutida tem exemplos de cidades. Para precisão oficial, mantenha uma fonte baseada em dados publicados/regulados pela Anatel.
