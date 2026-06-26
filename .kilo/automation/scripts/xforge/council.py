"""council.py - Council of Geniuses (GCF) data and helpers.

Static data: 38 geniuses (8 domains), 5 guardians, Devil's Advocate questions.
Used by `xforge council` subcommands.
"""

# 38 Geniuses in 8 domains
GENIUSES = {
    "fundamentos_computacao": [
        {"id": "AG001", "name": "Alan Turing", "expertise": "computabilidade"},
        {"id": "AG002", "name": "John von Neumann", "expertise": "arquitetura"},
        {"id": "AG003", "name": "Claude Shannon", "expertise": "teoria da informacao"},
    ],
    "engenharia_software": [
        {"id": "AG004", "name": "Donald Knuth", "expertise": "algoritmos"},
        {"id": "AG005", "name": "Edsger Dijkstra", "expertise": "complexidade, simplicidade"},
        {"id": "AG006", "name": "Barbara Liskov", "expertise": "abstracoes, contratos"},
        {"id": "AG007", "name": "Robert C. Martin", "expertise": "SOLID, Clean Code"},
    ],
    "linguagens_plataformas": [
        {"id": "AG008", "name": "Dennis Ritchie", "expertise": "C, eficiencia"},
        {"id": "AG009", "name": "Bjarne Stroustrup", "expertise": "C++"},
        {"id": "AG010", "name": "Anders Hejlsberg", "expertise": "C#, TypeScript"},
    ],
    "web_infra": [
        {"id": "AG011", "name": "Tim Berners-Lee", "expertise": "HTTP, interoperabilidade"},
        {"id": "AG012", "name": "Linus Torvalds", "expertise": "operacional, producao"},
    ],
    "inteligencia_artificial": [
        {"id": "AG013", "name": "Geoffrey Hinton", "expertise": "deep learning"},
        {"id": "AG014", "name": "Yann LeCun", "expertise": "modelagem IA"},
        {"id": "AG015", "name": "Demis Hassabis", "expertise": "AGI, multi-agent"},
    ],
    "produto_negocio": [
        {"id": "AG016", "name": "Steve Jobs", "expertise": "foco no usuario"},
        {"id": "AG017", "name": "Bill Gates", "expertise": "escala, plataforma"},
        {"id": "AG018", "name": "Steve Wozniak", "expertise": "praticidade tecnica"},
    ],
    "ux_ui_design": [
        {"id": "AG019", "name": "Don Norman", "expertise": "UX, affordance"},
        {"id": "AG020", "name": "Jakob Nielsen", "expertise": "usabilidade"},
        {"id": "AG021", "name": "Ben Shneiderman", "expertise": "HCI, dashboards"},
        {"id": "AG022", "name": "Dieter Rams", "expertise": "minimalismo"},
        {"id": "AG023", "name": "Jony Ive", "expertise": "premium"},
        {"id": "AG024", "name": "Susan Kare", "expertise": "iconografia"},
        {"id": "AG025", "name": "Brad Frost", "expertise": "Atomic Design"},
        {"id": "AG026", "name": "Nathan Curtis", "expertise": "design system governance"},
    ],
    "seguranca_privacidade": [
        {"id": "AG027", "name": "Whitfield Diffie", "expertise": "PKI"},
        {"id": "AG028", "name": "Martin Hellman", "expertise": "protocolos"},
        {"id": "AG029", "name": "Ron Rivest", "expertise": "RSA, assinaturas"},
        {"id": "AG030", "name": "Adi Shamir", "expertise": "ameacas"},
        {"id": "AG031", "name": "Leonard Adleman", "expertise": "complexidade"},
        {"id": "AG032", "name": "Bruce Schneier", "expertise": "engenharia seguranca"},
        {"id": "AG033", "name": "Ross Anderson", "expertise": "sistemas distribuidos"},
        {"id": "AG034", "name": "Dan Geer", "expertise": "risco cibermetrico"},
        {"id": "AG035", "name": "Kevin Mitnick", "expertise": "engenharia social"},
        {"id": "AG036", "name": "Charlie Miller", "expertise": "exploits"},
        {"id": "AG037", "name": "Ann Cavoukian", "expertise": "Privacy by Design"},
        {"id": "AG038", "name": "OWASP Collective", "expertise": "Top 10"},
    ],
}

# 5 Guardians
GUARDIANS = [
    {"id": "Architecture", "name": "Guardian Architecture", "checks": ['DDD/SOLID/Clean Architecture respeitados?', 'Bounded contexts claros?', 'Modularizacao adequada?']},
    {"id": "Simplicity", "name": "Guardian Simplicity", "checks": ['KISS respeitado?', 'Sem overengineering?', 'DRY aplicado sem abstracoes desnecessarias?', 'YAGNI respeitado?']},
    {"id": "Security", "name": "Guardian Security", "checks": ['Autenticacao implementada?', 'Autorizacao (RBAC/ABAC) verificada?', 'Dados sensiveis protegidos?', 'VETO se LGPD/GDPR violados']},
    {"id": "Quality", "name": "Guardian Quality", "checks": ['Cobertura de testes >= 85%?', 'Observabilidade presente?', 'Telemetria implementada?']},
    {"id": "Documentation", "name": "Guardian Documentation", "checks": ['Decisao documentada (DR)?', 'README + setup rapido presentes?', 'Glossario atualizado?', 'Indice de docs sincronizado?']},
]

# AG999 Devil\'s Advocate - 7 questions
DEVILS_ADVOCATE_QUESTIONS = [
    'Por que estamos fazendo isso?',
    'Existe alternativa melhor?',
    'Existe alternativa mais simples?',
    'Existe alternativa mais barata?',
    'Isso e necessidade real ou moda?',
    'Isso ainda fara sentido daqui a 5 anos?',
    'Qual e a maior critica possivel contra essa decisao?',
]

def get_all_geniuses():
    return [{**g, 'domain': d} for d, gs in GENIUSES.items() for g in gs]


def get_geniuses_by_domain(domain):
    return GENIUSES.get(domain, [])


def get_relevant_geniuses(topic):
    keywords = {
        "seguranca": ["seguranca_privacidade"],
        "security": ["seguranca_privacidade"],
        "lgpd": ["seguranca_privacidade"],
        "gdpr": ["seguranca_privacidade"],
        "ux": ["ux_ui_design"],
        "ui": ["ux_ui_design"],
        "design": ["ux_ui_design"],
        "performance": ["engenharia_software", "fundamentos_computacao"],
        "algoritmo": ["engenharia_software"],
        "arquitetura": ["engenharia_software"],
        "escala": ["fundamentos_computacao", "web_infra"],
        "ia": ["inteligencia_artificial"],
        "ml": ["inteligencia_artificial"],
        "ai": ["inteligencia_artificial"],
        "negocio": ["produto_negocio"],
        "produto": ["produto_negocio"],
        "deploy": ["web_infra"],
        "api": ["web_infra"],
        "http": ["web_infra"],
        "react": ["ux_ui_design", "linguagens_plataformas"],
        "vue": ["ux_ui_design", "linguagens_plataformas"],
        "python": ["linguagens_plataformas"],
        "rust": ["linguagens_plataformas"],
        "go": ["linguagens_plataformas"],
        "java": ["linguagens_plataformas"],
        "dotnet": ["linguagens_plataformas"],
        "typescript": ["linguagens_plataformas"],
    }
    matched = set()
    topic_lower = topic.lower()
    for kw, domain_list in keywords.items():
        if kw in topic_lower:
            for d in domain_list:
                matched.add(d)
    if not matched:
        matched.add("engenharia_software")

    result = []
    for domain in matched:
        for g in GENIUSES.get(domain, []):
            result.append((g, domain))
    return result[:7]


def list_domains():
    return {d: len(gs) for d, gs in GENIUSES.items()}
