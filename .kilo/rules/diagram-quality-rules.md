# Diagram Quality Rules

## Limites
- Max 15 nos por diagrama
- Max 3 niveis de profundidade
- Max 30 setas (senao, quebrar em multiplos)

## Padroes

### Cores
- Vermelho (#ff6b6b): erro, falha, bloqueio
- Verde (#51cf66): sucesso, ok, completo
- Amarelo (#ffd43b): atencao, warning, pendente
- Azul (#4dabf7): fluxo normal
- Cinza (#adb5bd): neutro, externo

### Setas
- Continua (-->) : fluxo normal
- Tracejada (-.->) : async, eventual
- Grossa (==>) : caminho feliz / critico

### Rotulos
- Verbos no infinitivo
- Verbo + substantivo
- Ex: Submete, Valida, Notifica

## Validacao
- [ ] Titulo presente
- [ ] Legenda se > 5 cores
- [ ] Direcao apropriada (TD para hierarquia, LR para fluxo)
- [ ] Renderiza sem erro
- [ ] Nomes unicos (sem ambiguidade)
