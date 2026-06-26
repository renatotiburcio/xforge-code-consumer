"""
cmd_council - Council of Geniuses (GCF) subcommands.
Modulo extraido de cli.py em v3.9.0 per DR-0082.
"""
from pathlib import Path

from council import GENIUSES, GUARDIANS, DEVILS_ADVOCATE_QUESTIONS, get_all_geniuses, get_relevant_geniuses, list_domains


def cmd_council(args):

    """Council of Geniuses (GCF) subcommands."""

    if args.council_cmd == "list":

        print("[XForge] Council of Geniuses (38 in 8 domains)")

        for domain, count in list_domains().items():

            print("[XForge]  " + domain + " (" + str(count) + ")")

            for g in GENIUSES[domain]:

                print("    " + g["id"] + " - " + g["name"])

        print("[XForge] Total: " + str(len(get_all_geniuses())) + " geniuses")

        print("[XForge] Guardians: " + str(len(GUARDIANS)))

        print("[XForge] Devils Advocate: " + str(len(DEVILS_ADVOCATE_QUESTIONS)) + " questions")

        return 0



    if args.council_cmd == "review":

        topic = args.topic or "general"

        print("[XForge] Council Review: " + topic)

        relevant = get_relevant_geniuses(topic)

        print("[XForge] " + str(len(relevant)) + " relevant geniuses:")

        for g, domain in relevant:

            print("  " + g["id"] + " - " + g["name"] + " - " + domain)

        for g, domain in relevant:

            print("--- " + g["id"] + ": " + g["name"] + " ---")

            for q in get_questions_for_genius(g["id"]):

                print("  ? " + q)

        return 0



    if args.council_cmd == "guards":

        print("[XForge] Guardian Validation (Security has VETO)")

        for guard in GUARDIANS:

            print("--- " + guard["name"] + " ---")

            for check in guard["checks"]:

                print("  [ ] " + check)

        return 0



    if args.council_cmd in ("devils-advocate", "da"):

        print("[XForge] Devils Advocate (AG999)")

        for q in DEVILS_ADVOCATE_QUESTIONS:

            print("  " + q)

        return 0



    if args.council_cmd == "ask":

        genius = find_genius(args.topic)

        if not genius:

            print("[XForge] Genius nao encontrado")

            return 1

        print("[XForge] " + genius["id"] + ": " + genius["name"] + " (" + genius["expertise"] + ")")

        for q in get_questions_for_genius(genius["id"]):

            print("  ? " + q)

        return 0



    return 1





def find_genius(genius_id):

    for domain, geniuses in GENIUSES.items():

        for g in geniuses:

            if g["id"] == genius_id:

                return {**g, "domain": domain}

    return None





def get_questions_for_genius(genius_id):

    Q = {

        "AG001": ["O problema e computavel?", "O algoritmo e finito?"],

        "AG002": ["A arquitetura escala?", "Single point of failure?"],

        "AG004": ["Complexidade Big-O?", "Algoritmo e elegante?"],

        "AG005": ["Pode ser mais simples?", "Estados desnecessarios?"],

        "AG007": ["Single Responsibility?", "Open/Closed?", "Liskov Substitution?", "Interface Segregation?", "Dependency Inversion?"],

        "AG012": ["Funciona em prod?", "Quem mantem?", "Ha testes reais?"],

        "AG016": ["Usuario precisa disso?", "Pode ser removido?"],

        "AG017": ["Escala?", "Unit economics?"],

        "AG019": ["Affordance clara?", "Feedback visivel?"],

        "AG020": ["Status visivel?", "Match mundo real?", "Usuario no controle?"],

        "AG025": ["Componentes atomicos?", "DS escalavel?"],

        "AG032": ["Defense in depth?", "Threat model?"],

        "AG037": ["LGPD/GDPR respeitados?", "Dados minimizados?"],

        "AG038": ["SQLi prevenido?", "XSS prevenido?", "CSRF/SSRF mitigados?"],

    }

    return Q.get(genius_id, ["Ha consideracoes deste genio para este topico?"])



def main():
    parser = argparse.ArgumentParser(
        prog="xforge",
        description="XForge CLI v3.0 - Installable Toolkit",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="cmd", help="Comandos disponiveis")

    p_init = sub.add_parser("init", help="Bootstrap .kilo + .xforge no projeto atual")
    p_init.add_argument("--template", help="Template de projeto")
    p_init.add_argument("--analyze", action="store_true", help="Rodar recognize apos init")
    p_init.add_argument("--force", action="store_true", help="Sobrescrever existentes")
    p_init.add_argument("--interactive", "-i", action="store_true", help="Modo wizard (pergunta nome, packs, etc)")

    sub.add_parser("recognize", help="Analisar projeto e gerar PROJECT-DNA")
    p_status = sub.add_parser("status", help="Mostrar status de adocao + metricas")
    p_status.add_argument("--log", action="store_true", help="Registrar snapshot em .xforge/.adoption.json")
    sub.add_parser("doctor", help="Validar setup")
    p_upgrade = sub.add_parser("upgrade", help="Atualizar .kilo + .xforge")
    p_upgrade.add_argument("--force", action="store_true", help="Sobrescrever arquivos modificados")
    p_upgrade.add_argument("--remote", action="store_true", help="[v3.4+] Baixar upgrade do GitHub Releases API")
    p_upgrade.add_argument("--check", action="store_true", help="[v3.4+] Apenas verificar se ha update")
    p_upgrade.add_argument("--changelog", action="store_true", help="[v3.4+] Mostrar changelog do release remoto")
    p_upgrade.add_argument("--yes", action="store_true", help="[v3.4+] Upgrade sem prompt")
    p_upgrade.add_argument("--dry-run", action="store_true", help="[v3.4+] Mostrar sem aplicar")

    p_new = sub.add_parser("new", help="Criar novo projeto com template")
    p_new.add_argument("stack", help="Stack")
    p_new.add_argument("--name", help="Nome do projeto")

    sub.add_parser("backup", help="Backup de .xforge state")
    p_pack = sub.add_parser("pack", help="Marketplace packs (list, info, install, remove)")
    p_pack.add_argument("pack_cmd", choices=["list", "search", "info", "install", "remove", "update", "upgrade"], help="Comando")
    p_pack.add_argument("pack_id", nargs="?", help="Pack ID")
    p_pack.add_argument("--source", help="Source URL/path para install")
    p_pack.add_argument("--force", action="store_true", help="Forcar instalacao/reinstalacao")

    p_restore = sub.add_parser("restore", help="Restore de backup")
    p_council = sub.add_parser("council", help="Council of Geniuses (GCF) subcommands")
    p_council.add_argument("council_cmd", choices=["list", "review", "guards", "devils-advocate", "da", "ask"], help="Comando do Council")
    p_council.add_argument("topic", nargs="?", help="Topico / path / genius_id")
    p_restore.add_argument("--index", type=int, dest="backup_index")

    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        return 1

    commands = {
        "init": cmd_init,
        "recognize": cmd_recognize,
        "status": cmd_status,
        "doctor": cmd_doctor,
        "upgrade": cmd_upgrade,
        "new": cmd_new,
        "backup": cmd_backup,
        "pack": cmd_pack,
        "council": cmd_council,
        "restore": cmd_restore,
        "council": cmd_council,
    }

    return commands[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())

