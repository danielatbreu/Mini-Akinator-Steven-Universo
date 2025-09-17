import random
import sys
from collections import Counter

MIN_PERGUNTAS = 5
MAX_PERGUNTAS = 15

# --- Base: personagem -> [nivel0, nivel1, nivel2, nivel3] ---
personagens = {
    "Steven":  ["humano", "camiseta_vermelha", "meio_humano", "pedra_umbigo"],
    "Garnet":  ["gem", "oculos_escuros", "duas_pedras", "fusao_ruby_sapphire"],
    "Ametista":["gem", "baixo_robusto", "chicote", "pedra_peito"],
    "Pérola":  ["gem", "lanca", "perfeccionista", "pedra_testa"],
    "Rose":    ["gem", "cabelo_rosa_longo", "lider_crystal_gems", "pedra_umbigo"],
    "Peridot": ["gem", "tecnologia_extensoes", "pele_verde", "perdeu_extensoes"],
    "Lápis":   ["gem", "controla_agua", "asas_agua", "presa_espelho"],
    "Connie":  ["humano", "usa_oculos", "espada", "amiga_steven"],
    "Greg":    ["humano", "musico", "pai_steven", "van_amarela"],
    "Lars":    ["humano", "padaria", "cabelo_rosa", "capitao_offcolors"]
}

# --- Texto das perguntas (cada chave é uma "característica") ---
perguntas_texto = {
    "gem": "O personagem é uma Gem?",
    "humano": "O personagem é humano (não é uma Gem)?",
    "meio_humano": "O personagem é meio-humano (metade Gem, metade humano)?",
    "oculos_escuros": "Ele usa óculos escuros quase sempre?",
    "usa_oculos": "Ele usa óculos?",
    "cabelo_rosa_longo": "Tem cabelos longos e cor-de-rosa?",
    "cabelo_rosa": "Tem cabelo rosa?",
    "camiseta_vermelha": "Usa uma camiseta vermelha com estrela?",
    "pedra_umbigo": "A pedra dele(a) fica no umbigo?",
    "duas_pedras": "Possui duas gemas (uma em cada mão)?",
    "fusao_ruby_sapphire": "É a fusão de Ruby e Safira?",
    "baixo_robusto": "Tem corpo mais baixo e robusto?",
    "chicote": "Sua arma principal é um chicote?",
    "pedra_peito": "A pedra dele(a) fica no peito?",
    "lanca": "Sua arma principal é uma lança?",
    "perfeccionista": "É muito organizado(a) e perfeccionista?",
    "pedra_testa": "A pedra dele(a) fica na testa?",
    "lider_crystal_gems": "Foi líder das Crystal Gems?",
    "tecnologia_extensoes": "Usava extensões tecnológicas (membros robóticos)?",
    "pele_verde": "Tem pele verde?",
    "perdeu_extensoes": "Perdeu suas extensões tecnológicas em algum momento?",
    "controla_agua": "Consegue controlar a água?",
    "asas_agua": "Já criou asas de água?",
    "presa_espelho": "Ficou presa em um espelho por muito tempo?",
    "espada": "Aprendeu a lutar com espada?",
    "amiga_steven": "É amiga próxima do Steven?",
    "musico": "Trabalhou como músico?",
    "pai_steven": "É pai do Steven?",
    "van_amarela": "Possui uma van amarela?",
    "padaria": "Trabalha (ou trabalhou) em uma padaria?",
    "capitao_offcolors": "Virou capitão dos Off-Colors?"
}

# --- Mapeia cada característica ao seu nível (0..3) para fácil procura ---
attr_to_level = {}
for nome, attrs in personagens.items():
    for lvl, attr in enumerate(attrs):
        # guarda sempre o menor nível encontrado (pergunta mais fácil primeiro)
        if attr in attr_to_level:
            attr_to_level[attr] = min(attr_to_level[attr], lvl)
        else:
            attr_to_level[attr] = lvl

niveis = ["Fácil", "Médio", "Médio-Difícil", "Difícil"]

# estado do jogo
restantes = list(personagens.keys())
respondidas = {}   # attr -> True/False (resposta do usuário)
perguntas_feitas = set()
qtd_perguntas = 0

def ler_resposta():
    """Lê e valida resposta (1 = sim, 2 = não)."""
    r = input("Resposta (1 = SIM / 2 = NÃO): ").strip()
    while r not in ("1", "2"):
        r = input("Inválido. Digite 1 para SIM ou 2 para NÃO: ").strip()
    return r == "1"

def contar_por_attr(level_index, attr, candidatos):
    """Conta quantos candidatos têm 'attr' no level_index."""
    return sum(1 for p in candidatos if personagens[p][level_index] == attr)

def escolher_melhor_atributo(atributos, candidatos, level_index):
    """
    Escolhe o atributo que melhor divide o conjunto 'candidatos' (contagem mais próxima da metade).
    atributos: lista de atributos possíveis neste nível (não perguntados ainda).
    """
    if not atributos:
        return None
    total = len(candidatos)
    # só atributos que realmente separam (count != 0 e != total)
    opcoes = []
    for a in atributos:
        c = contar_por_attr(level_index, a, candidatos)
        if 0 < c < total:
            opcoes.append((a, c))
    if not opcoes:
        return None
    # minimizar |c - total/2|
    melhor = min(opcoes, key=lambda ac: abs(ac[1] - total/2))
    return melhor[0]

def perguntar_e_filtrar(attr, nivel_idx):
    """Faz a pergunta 'attr' (nível nivel_idx), atualiza respondidas, perguntas_feitas, qtd_perguntas e retorna novos 'restantes'."""
    global qtd_perguntas, restantes
    print(f"\nPergunta {qtd_perguntas+1} ({niveis[nivel_idx]}): {perguntas_texto.get(attr, attr)}")
    resposta_sim = ler_resposta()
    respondidas[attr] = resposta_sim
    perguntas_feitas.add(attr)
    qtd_perguntas += 1

    if resposta_sim:
        # manter só quem tem esse atributo no nível
        restantes = [p for p in restantes if personagens[p][nivel_idx] == attr]
    else:
        # eliminar quem tem esse atributo no nível
        restantes = [p for p in restantes if personagens[p][nivel_idx] != attr]

    # Mostra estado (compacto)
    if len(restantes) <= 6:
        print("-> Ainda possíveis:", ", ".join(restantes))
    else:
        print("->", len(restantes), "personagens ainda possíveis.")
    return

# --- Início do jogo ---
print("=== Mini-Akinator: Steven Universe (versão avançada) ===")
print("Pense em UM personagem da lista (não fale em voz alta):")
print(", ".join(restantes))
print("\nResponda apenas com 1 (SIM) ou 2 (NÃO). Vamos começar!\n")

# Loop por níveis
for lvl_idx in range(4):
    # enquanto houver atributos úteis neste nível e não atingir MAX_PERGUNTAS
    while True:
        if qtd_perguntas >= MAX_PERGUNTAS:
            break

        # calcula atributos possíveis neste nível entre os restantes
        attrs_possiveis = list({personagens[p][lvl_idx] for p in restantes})
        # remove já perguntados
        attrs_possiveis = [a for a in attrs_possiveis if a not in perguntas_feitas]

        # se não houver atributos possíveis, saia do nível
        if not attrs_possiveis:
            break

        # escolhe atributo informativo (melhor divisão)
        escolhido = escolher_melhor_atributo(attrs_possiveis, restantes, lvl_idx)

        # se não houver atributo informativo, paramos o nível
        if not escolhido:
            break

        # pergunta e filtra
        perguntar_e_filtrar(escolhido, lvl_idx)

        # checa condições
        if len(restantes) == 0:
            print("\nNenhum personagem corresponde às respostas fornecidas. Encerrando.")
            sys.exit(0)

        if len(restantes) == 1:
            candidato = restantes[0]
            # precisa confirmar a pergunta difícil desse candidato antes de declarar
            diff_attr = personagens[candidato][3]
            # se já foi perguntada e confirmada, só precisa obedecer min perguntas
            if diff_attr in respondidas and respondidas[diff_attr] and qtd_perguntas >= MIN_PERGUNTAS:
                print(f"\n✅ Descobri! Seu personagem é: {candidato}")
                sys.exit(0)
            # se diff_attr ainda não foi perguntada, façamos a confirmação seguindo a regra MIN
            if diff_attr not in perguntas_feitas:
                # primeiro, garanto que até o momento a gente tenha feito perguntas razoáveis.
                # vou fazer perguntas preferenciais: atributos do próprio candidato (níveis 0..2) que ainda não foram perguntados,
                # até atingir MIN_PERGUNTAS - 1 (assim a pergunta difícil será a MIN-ésima).
                for pref_lvl in range(3):
                    if qtd_perguntas >= MAX_PERGUNTAS:
                        break
                    attr_pref = personagens[candidato][pref_lvl]
                    if attr_pref not in perguntas_feitas and qtd_perguntas < (MIN_PERGUNTAS - 1):
                        perguntar_e_filtrar(attr_pref, pref_lvl)
                        if len(restantes) != 1:
                            # se a resposta eliminou o candidato, interrompe e volta ao fluxo normal
                            break

                # Se ainda faltarem perguntas pra chegar em MIN_PERGUNTAS - 1, perguntar outros atributos não usados
                all_unasked = [a for a in perguntas_texto.keys() if a not in perguntas_feitas and a != diff_attr]
                ai = 0
                while qtd_perguntas < (MIN_PERGUNTAS - 1) and ai < len(all_unasked) and len(restantes) == 1:
                    a = all_unasked[ai]; ai += 1
                    lvl_a = attr_to_level.get(a, 0)
                    perguntar_e_filtrar(a, lvl_a)

                # por fim, pergunte a pergunta difícil do candidato (confirmação final)
                if len(restantes) == 1 and diff_attr not in perguntas_feitas and qtd_perguntas < MAX_PERGUNTAS:
                    perguntar_e_filtrar(diff_attr, 3)

                # após perguntar diff_attr, se confirmado e MIN cumprido, revelar
                if diff_attr in respondidas and respondidas[diff_attr] and qtd_perguntas >= MIN_PERGUNTAS and len(restantes) == 1:
                    print(f"\n✅ Descobri! Seu personagem é: {candidato}")
                    sys.exit(0)
                # se diff_attr foi perguntado e foi NÃO, candidato foi eliminado; continuar
                if len(restantes) == 0:
                    print("\nNenhum personagem corresponde às respostas fornecidas. Encerrando.")
                    sys.exit(0)
                # se diff_attr foi perguntado e foi NÃO, o candidato foi eliminado e o loop continua normalmente
            else:
                # diff_attr já perguntada antes, mas talvez MIN não foi alcançado
                if respondidas.get(diff_attr) and qtd_perguntas >= MIN_PERGUNTAS:
                    print(f"\n✅ Descobri! Seu personagem é: {candidato}")
                    sys.exit(0)
                # caso diff_attr já respondida com SIM mas qtd < MIN, continuamos com perguntas (o fluxo principal fará isso)
        # fim len(restantes)==1 tratamento

    # se sair do while do nível, vai para próximo nível
    if qtd_perguntas >= MAX_PERGUNTAS:
        break

# fim dos níveis / limite de perguntas
print("\n--- Fim das perguntas ---")
if len(restantes) == 1:
    print("Com base nas respostas, seu personagem é:", restantes[0])
elif len(restantes) > 1:
    print("Não consegui adivinhar com certeza dentro do limite de perguntas.")
    print("Possíveis candidatos restantes:", ", ".join(restantes))
else:
    print("Nenhum personagem corresponde às respostas fornecidas.")