"""
XForge CLI v3.9 - Installable Toolkit

Comandos:
  xforge init [--template T] [--analyze]   Bootstrap .kilo + .xforge
  xforge recognize                         Analyze project, generate PROJECT-DNA
  xforge status                            Show adoption status
  xforge doctor                            Validate setup
  xforge upgrade                           Update .kilo + .xforge
  xforge new STACK                         Create new project with template
  xforge backup                            Backup .xforge state
  xforge restore                           Restore from backup
  xforge pack CMD [PACK_ID]                Marketplace packs
  xforge council CMD [TOPIC]               Council of Geniuses (GCF)

Uso:
  cd meu-projeto
  xforge init --analyze
  xforge doctor
"""

__version__ = "3.9.0"