from __future__ import annotations

from typing import List, Optional, Dict, Any

from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import strawberry
from strawberry.flask.views import GraphQLView


DDD_DATA: Dict[int, Dict[str, Any]] = {
    11: {"uf": "SP", "estado": "São Paulo", "regiao": "RMSP e entorno", "cidades": ["São Paulo", "Guarulhos", "Osasco"]},
    12: {"uf": "SP", "estado": "São Paulo", "regiao": "Vale do Paraíba e Litoral Norte", "cidades": ["São José dos Campos", "Taubaté", "Caraguatatuba"]},
    13: {"uf": "SP", "estado": "São Paulo", "regiao": "Baixada Santista e Vale do Ribeira", "cidades": ["Santos", "São Vicente", "Registro"]},
    14: {"uf": "SP", "estado": "São Paulo", "regiao": "Centro-oeste paulista", "cidades": ["Bauru", "Marília", "Botucatu"]},
    15: {"uf": "SP", "estado": "São Paulo", "regiao": "Sorocaba e sudoeste paulista", "cidades": ["Sorocaba", "Itapetininga", "Itapeva"]},
    16: {"uf": "SP", "estado": "São Paulo", "regiao": "Nordeste paulista", "cidades": ["Ribeirão Preto", "Franca", "São Carlos"]},
    17: {"uf": "SP", "estado": "São Paulo", "regiao": "Noroeste paulista", "cidades": ["São José do Rio Preto", "Votuporanga", "Catanduva"]},
    18: {"uf": "SP", "estado": "São Paulo", "regiao": "Oeste paulista", "cidades": ["Presidente Prudente", "Araçatuba", "Assis"]},
    19: {"uf": "SP", "estado": "São Paulo", "regiao": "Campinas e região", "cidades": ["Campinas", "Piracicaba", "Limeira"]},

    21: {"uf": "RJ", "estado": "Rio de Janeiro", "regiao": "Região Metropolitana do Rio", "cidades": ["Rio de Janeiro", "Niterói", "Duque de Caxias"]},
    22: {"uf": "RJ", "estado": "Rio de Janeiro", "regiao": "Norte e Noroeste Fluminense", "cidades": ["Campos dos Goytacazes", "Macaé", "Itaperuna"]},
    24: {"uf": "RJ", "estado": "Rio de Janeiro", "regiao": "Sul Fluminense e Centro-Sul", "cidades": ["Volta Redonda", "Barra Mansa", "Resende"]},

    27: {"uf": "ES", "estado": "Espírito Santo", "regiao": "Grande Vitória e parte do litoral", "cidades": ["Vitória", "Vila Velha", "Serra"]},
    28: {"uf": "ES", "estado": "Espírito Santo", "regiao": "Sul do estado", "cidades": ["Cachoeiro de Itapemirim", "Alegre", "Marataízes"]},

    31: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Região Metropolitana de BH", "cidades": ["Belo Horizonte", "Contagem", "Betim"]},
    32: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Zona da Mata", "cidades": ["Juiz de Fora", "Barbacena", "Viçosa"]},
    33: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Vale do Rio Doce e Mucuri", "cidades": ["Governador Valadares", "Teófilo Otoni", "Caratinga"]},
    34: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Triângulo, Alto Paranaíba", "cidades": ["Uberlândia", "Uberaba", "Patos de Minas"]},
    35: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Sul e Sudoeste de MG", "cidades": ["Poços de Caldas", "Pouso Alegre", "Varginha"]},
    37: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Centro-Oeste de MG", "cidades": ["Divinópolis", "Itaúna", "Formiga"]},
    38: {"uf": "MG", "estado": "Minas Gerais", "regiao": "Norte de MG", "cidades": ["Montes Claros", "Janaúba", "Pirapora"]},

    41: {"uf": "PR", "estado": "Paraná", "regiao": "Curitiba e litoral", "cidades": ["Curitiba", "São José dos Pinhais", "Paranaguá"]},
    42: {"uf": "PR", "estado": "Paraná", "regiao": "Campos Gerais", "cidades": ["Ponta Grossa", "Guarapuava", "Telêmaco Borba"]},
    43: {"uf": "PR", "estado": "Paraná", "regiao": "Norte do PR", "cidades": ["Londrina", "Apucarana", "Cornélio Procópio"]},
    44: {"uf": "PR", "estado": "Paraná", "regiao": "Noroeste do PR", "cidades": ["Maringá", "Umuarama", "Paranavaí"]},
    45: {"uf": "PR", "estado": "Paraná", "regiao": "Oeste do PR", "cidades": ["Foz do Iguaçu", "Cascavel", "Toledo"]},
    46: {"uf": "PR", "estado": "Paraná", "regiao": "Sudoeste do PR", "cidades": ["Pato Branco", "Francisco Beltrão", "Dois Vizinhos"]},

    47: {"uf": "SC", "estado": "Santa Catarina", "regiao": "Norte e Vale do Itajaí", "cidades": ["Joinville", "Blumenau", "Itajaí"]},
    48: {"uf": "SC", "estado": "Santa Catarina", "regiao": "Grande Florianópolis e sul/litoral", "cidades": ["Florianópolis", "São José", "Palhoça"]},
    49: {"uf": "SC", "estado": "Santa Catarina", "regiao": "Oeste e Serra", "cidades": ["Chapecó", "Lages", "Joaçaba"]},

    51: {"uf": "RS", "estado": "Rio Grande do Sul", "regiao": "Grande Porto Alegre", "cidades": ["Porto Alegre", "Canoas", "Novo Hamburgo"]},
    53: {"uf": "RS", "estado": "Rio Grande do Sul", "regiao": "Sul do RS", "cidades": ["Pelotas", "Rio Grande", "Bagé"]},
    54: {"uf": "RS", "estado": "Rio Grande do Sul", "regiao": "Serra Gaúcha", "cidades": ["Caxias do Sul", "Bento Gonçalves", "Passo Fundo"]},
    55: {"uf": "RS", "estado": "Rio Grande do Sul", "regiao": "Oeste e Fronteira", "cidades": ["Santa Maria", "Uruguaiana", "Santana do Livramento"]},

    61: {"uf": "DF", "estado": "Distrito Federal", "regiao": "DF e entorno", "cidades": ["Brasília"]},
    62: {"uf": "GO", "estado": "Goiás", "regiao": "Centro de GO", "cidades": ["Goiânia", "Anápolis", "Aparecida de Goiânia"]},
    63: {"uf": "TO", "estado": "Tocantins", "regiao": "TO", "cidades": ["Palmas", "Araguaína", "Gurupi"]},
    64: {"uf": "GO", "estado": "Goiás", "regiao": "Sul de GO", "cidades": ["Rio Verde", "Itumbiara", "Catalão"]},
    65: {"uf": "MT", "estado": "Mato Grosso", "regiao": "Cuiabá e região", "cidades": ["Cuiabá", "Várzea Grande"]},
    66: {"uf": "MT", "estado": "Mato Grosso", "regiao": "Interior de MT", "cidades": ["Rondonópolis", "Sinop", "Sorriso"]},
    67: {"uf": "MS", "estado": "Mato Grosso do Sul", "regiao": "MS", "cidades": ["Campo Grande", "Dourados", "Corumbá"]},

    68: {"uf": "AC", "estado": "Acre", "regiao": "AC", "cidades": ["Rio Branco", "Cruzeiro do Sul"]},
    69: {"uf": "RO", "estado": "Rondônia", "regiao": "RO", "cidades": ["Porto Velho", "Ji-Paraná"]},

    71: {"uf": "BA", "estado": "Bahia", "regiao": "Salvador e RMS", "cidades": ["Salvador", "Lauro de Freitas"]},
    73: {"uf": "BA", "estado": "Bahia", "regiao": "Sul da BA", "cidades": ["Ilhéus", "Itabuna", "Porto Seguro"]},
    74: {"uf": "BA", "estado": "Bahia", "regiao": "Norte da BA", "cidades": ["Juazeiro", "Jacobina"]},
    75: {"uf": "BA", "estado": "Bahia", "regiao": "Centro-norte da BA", "cidades": ["Feira de Santana", "Alagoinhas"]},
    77: {"uf": "BA", "estado": "Bahia", "regiao": "Sudoeste e oeste da BA", "cidades": ["Vitória da Conquista", "Barreiras"]},

    79: {"uf": "SE", "estado": "Sergipe", "regiao": "SE", "cidades": ["Aracaju"]},
    81: {"uf": "PE", "estado": "Pernambuco", "regiao": "Recife e região", "cidades": ["Recife", "Olinda", "Jaboatão"]},
    82: {"uf": "AL", "estado": "Alagoas", "regiao": "AL", "cidades": ["Maceió", "Arapiraca"]},
    83: {"uf": "PB", "estado": "Paraíba", "regiao": "PB", "cidades": ["João Pessoa", "Campina Grande"]},
    84: {"uf": "RN", "estado": "Rio Grande do Norte", "regiao": "RN", "cidades": ["Natal", "Mossoró"]},
    85: {"uf": "CE", "estado": "Ceará", "regiao": "Fortaleza e região", "cidades": ["Fortaleza", "Caucaia"]},
    86: {"uf": "PI", "estado": "Piauí", "regiao": "Teresina e centro-norte", "cidades": ["Teresina"]},
    87: {"uf": "PE", "estado": "Pernambuco", "regiao": "Interior de PE", "cidades": ["Petrolina", "Garanhuns", "Caruaru"]},
    88: {"uf": "CE", "estado": "Ceará", "regiao": "Interior do CE", "cidades": ["Sobral", "Juazeiro do Norte"]},
    89: {"uf": "PI", "estado": "Piauí", "regiao": "Sul do PI", "cidades": ["Picos", "Floriano"]},

    91: {"uf": "PA", "estado": "Pará", "regiao": "Belém e região", "cidades": ["Belém", "Ananindeua"]},
    92: {"uf": "AM", "estado": "Amazonas", "regiao": "Manaus", "cidades": ["Manaus"]},
    93: {"uf": "PA", "estado": "Pará", "regiao": "Oeste do PA", "cidades": ["Santarém", "Altamira"]},
    94: {"uf": "PA", "estado": "Pará", "regiao": "Sudeste do PA", "cidades": ["Marabá", "Parauapebas"]},
    95: {"uf": "RR", "estado": "Roraima", "regiao": "RR", "cidades": ["Boa Vista"]},
    96: {"uf": "AP", "estado": "Amapá", "regiao": "AP", "cidades": ["Macapá"]},
    97: {"uf": "AM", "estado": "Amazonas", "regiao": "Interior do AM", "cidades": ["Tefé", "Parintins"]},
    98: {"uf": "MA", "estado": "Maranhão", "regiao": "São Luís e região", "cidades": ["São Luís"]},
    99: {"uf": "MA", "estado": "Maranhão", "regiao": "Sul do MA", "cidades": ["Imperatriz"]},
}


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _parse_int(v: str) -> Optional[int]:
    try:
        return int(str(v).strip())
    except Exception:
        return None


def ddd_to_dict(code: int) -> Optional[Dict[str, Any]]:
    row = DDD_DATA.get(code)
    if not row:
        return None
    return {"code": code, **row}


# GraphQL
@strawberry.type
class DDDInfo:
    code: int
    uf: str
    estado: str
    regiao: str
    cidades: List[str]


def as_info(code: int) -> Optional[DDDInfo]:
    d = ddd_to_dict(code)
    return DDDInfo(**d) if d else None


@strawberry.type
class Query:
    @strawberry.field
    def ddd(self, code: int) -> Optional[DDDInfo]:
        return as_info(code)

    @strawberry.field
    def ddds(self) -> List[DDDInfo]:
        out: List[DDDInfo] = []
        for code in sorted(DDD_DATA.keys()):
            info = as_info(code)
            if info:
                out.append(info)
        return out

    @strawberry.field
    def search(self, text: str) -> List[DDDInfo]:
        t = _norm(text)
        if not t:
            return []
        hits: List[DDDInfo] = []
        for code, row in DDD_DATA.items():
            hay = " ".join([str(code), row["uf"], row["estado"], row["regiao"], " ".join(row["cidades"])]).lower()
            if t in hay:
                info = as_info(code)
                if info:
                    hits.append(info)
        return hits


schema = strawberry.Schema(query=Query)

app = Flask(__name__)

# Flasgger: template (conteúdo do swagger) + config (inclui specs)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "DDD Brasil API",
        "description": "REST + GraphQL para consulta de DDDs do Brasil",
        "version": "1.0.0",
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

Swagger(app, config=swagger_config, template=swagger_template)

# GraphQL endpoint (com GraphiQL)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True),
)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/ddd/<code>")
@swag_from({
    "tags": ["DDD"],
    "parameters": [
        {"name": "code", "in": "path", "type": "integer", "required": True, "description": "Código DDD, ex: 21"},
    ],
    "responses": {
        200: {
            "description": "DDD encontrado",
            "schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "uf": {"type": "string"},
                    "estado": {"type": "string"},
                    "regiao": {"type": "string"},
                    "cidades": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        400: {"description": "DDD inválido"},
        404: {"description": "DDD não encontrado"},
    },
})
def rest_get_ddd(code: str):
    c = _parse_int(code)
    if c is None:
        return jsonify({"error": "invalid_code", "message": "DDD deve ser um inteiro"}), 400
    d = ddd_to_dict(c)
    if not d:
        return jsonify({"error": "not_found", "message": f"DDD {c} não encontrado"}), 404
    return jsonify(d)


@app.get("/api/ddds")
@swag_from({
    "tags": ["DDD"],
    "parameters": [
        {"name": "uf", "in": "query", "type": "string", "required": False, "description": "Filtrar por UF, ex: SP"},
        {"name": "estado", "in": "query", "type": "string", "required": False, "description": "Filtro parcial por estado"},
        {"name": "q", "in": "query", "type": "string", "required": False, "description": "Busca livre em UF, estado, região, cidades"},
    ],
    "responses": {
        200: {
            "description": "Lista de DDDs",
            "schema": {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"},
                    "items": {"type": "array", "items": {"type": "object"}},
                },
            },
        }
    },
})
def rest_list_ddds():
    uf = _norm(request.args.get("uf", ""))
    estado = _norm(request.args.get("estado", ""))
    q = _norm(request.args.get("q", ""))

    items: List[Dict[str, Any]] = []
    for code in sorted(DDD_DATA.keys()):
        d = ddd_to_dict(code)
        if not d:
            continue

        if uf and d["uf"].lower() != uf:
            continue
        if estado and estado not in d["estado"].lower():
            continue
        if q:
            hay = " ".join([str(d["code"]), d["uf"], d["estado"], d["regiao"], " ".join(d["cidades"])]).lower()
            if q not in hay:
                continue

        items.append(d)

    return jsonify({"count": len(items), "items": items})


@app.get("/api/search")
@swag_from({
    "tags": ["DDD"],
    "parameters": [
        {"name": "q", "in": "query", "type": "string", "required": True, "description": "Texto para busca, ex: rio"},
    ],
    "responses": {
        200: {"description": "Resultados da busca"},
        400: {"description": "Parâmetro q ausente"},
    },
})
def rest_search():
    q = _norm(request.args.get("q", ""))
    if not q:
        return jsonify({"error": "missing_q", "message": "Use ?q=texto"}), 400

    hits: List[Dict[str, Any]] = []
    for code in sorted(DDD_DATA.keys()):
        row = DDD_DATA[code]
        hay = " ".join([str(code), row["uf"], row["estado"], row["regiao"], " ".join(row["cidades"])]).lower()
        if q in hay:
            d = ddd_to_dict(code)
            if d:
                hits.append(d)

    return jsonify({"count": len(hits), "items": hits})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
