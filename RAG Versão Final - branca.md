

*Os meus alunos do Instituto Federal de Goiás, amo vocês\!*

**Copyright © 2025**

2

**Sumário**

1. [Gerando Revoluções](#bookmark=id.rmusfbbjhgm9)	6  
   1. [Quando usar RAG](#bookmark=id.oj3eceyfscvc)	8  
   2. [Decodificando a Arquitetura: Os Bastidores do RAG](#bookmark=id.vv1lxb7jf43e)	9  
   3. [Um RAG Simples](#bookmark=id.sv1c2qg8n1ah)	13  
   4. [Ele pode lembrar, RAG com Memória](#bookmark=id.t6sw4na2uqro)	14  
   5. [O RAG Autônomo: Agent RAG](#bookmark=id.ot8mn6y0m7ex)	15  
   6. [O RAG Corretivo: CRAG](#bookmark=id.dfmrkjtp21uh)	16  
   7. [O RAG Adaptativo: Adaptive RAG](#bookmark=id.t03fy9nqf0lq)	18  
   8. [O RAG em Grafos: GraphRAG](#bookmark=id.bsnk5wi01kaj)	19  
   9. [O RAG Híbrido: Hybrid RAG](#bookmark=id.dzsydblw4nfl)	20  
   10. [O RAG-Fusion: Reciprocal Rank Fusion (RRF)](#bookmark=id.afhy73hhu6vs)	22  
   11. [Hypothetical Document Embedding](#bookmark=id.ibglew9ed6ym)	23  
2. [O RAG Clássico](#bookmark=id.wen5w9klbt0q)	25  
   1. [O que é um Corpus de Textos](#bookmark=id.ynb0q6qxmpeu)	27  
   2. [O Fluxo do RAG](#bookmark=id.lcamfaq6zx2d)	28  
   3. [A Fase do Indexador](#bookmark=id.fuhzgrl6gmd3)	30  
   4. [Lendo e convertendo](#bookmark=id.8juj5axc92ue)	31  
   5. [Chunking](#bookmark=id.a1o2qcutrkka)	35  
   6. [Criação de Embeddings](#bookmark=id.cuxr6c0aj2)	37  
   7. [Banco de dados Vetorial](#bookmark=id.2d83an9yv59p)	41  
   8. [Nossa Classe de Encoder](#bookmark=id.io61ni3m3ncp)	42  
   9. [Recuperando conhecimento](#bookmark=id.c4fufoqlsc0m)	47  
   10. [Aumento de informação](#bookmark=id.1z4vscbypxja)	51  
   11. [Gerando a Resposta](#bookmark=id.gz2spbde4jij)	53  
   12. [Rodando com Streamlit](#bookmark=id.jaujum6vrr4t)	55  
   13. [Exercícios](#bookmark=id.g3sbpqwu9pn)	58

       3

       

3. [Rag com Memória](#bookmark=id.ht6pw3opp1o3)	60  
   1. [Criando a Memória com o Redis](#bookmark=id.oryce63tgukp)	63  
   2. [Redis no Docker](#bookmark=id.etpssg8jnozn)	64  
   3. [Instalando o Redis](#bookmark=id.t7k1fa6yaf2a)	68  
   4. [Criando a Mémória](#bookmark=id.ps7m99s3cvjj)	70  
   5. [Adicionando a Memória ao RAG](#bookmark=id.wcpo5vtgf6vi)	75  
   6. [Exercícios](#bookmark=id.4km426uxm27n)	80  
4. [RAG Autônomo com Agentic RAG](#bookmark=id.bhs3eghp4z9r)	82  
   1. [AgenticRAG](#bookmark=id.9xw4rz1k1g4u)	83  
   2. [Classe de Registro de Datasets](#bookmark=id.watnjt15zhmv)	86  
   3. [Agente Abstrato](#bookmark=id.1blxpowuwbna)	88  
   4. [Agente com API da LLM](#bookmark=id.i16c2v40lioh)	90  
   5. [Agentic RAG com CrewAI](#bookmark=id.2sgjn1d4sn5f)	96  
   6. [Executando o Agentic RAG](#bookmark=id.hgfvr1v7sco3)	102  
   7. [Exercícios](#bookmark=id.hoqv8ldydxqw)	104  
5. [O RAG em Grafos: GraphRAG](#bookmark=id.rhb6lsxvhb1f)	106  
   1. [Do Vetor ao Grafo](#bookmark=id.dss497oguxx4)	107  
   2. [Definição de grafo](#bookmark=id.bnzz6j3nvswu)	107  
   3. [De Textos para Grafos](#bookmark=id.kf2yhm160xvl)	110  
      [5.4 Neo4j](#bookmark=id.txv37okdy5a1)	114  
   1. [Instalando o Neo4J no Docker](#bookmark=id.ix7gurdatfq3)	114  
   2. [Cypher: Conversando com o Grafo](#bookmark=id.m1eyw32093uv)	119  
   3. [Microsoft GraphRAG](#bookmark=id.csmqscnen4l7)	123  
   4. [Extração automática de entidades e Relacionamentos](#bookmark=id.pbwmkx8awkyq)	125  
   5. [Gerando Comunidades no Neo4J](#bookmark=id.14eyzgqdjitl)	126  
   6. [Mostrando os grafos da comunidade](#bookmark=id.eij8mvnjt0w0)	131  
   7. [Gerando resumos das comunidades](#bookmark=id.9fahukbufn6c)	133  
   8. [Detecção automática de entidades](#bookmark=id.2qgarqcdpuko)	137  
   9. [Definindo os Grupos de Chunks](#bookmark=id.nj7gdksm6ucb)	139  
   10. [Um problema sério com GraphRAG](#bookmark=id.ygf8gvfhfba)	145  
1. [O RAG Híbrido](#bookmark=id.wzw5kf26so47)	147  
   1. [Indexação no Hybrid RAG](#bookmark=id.8y3z7slc71jz)	148  
   2. [A consulta no Hybrid RAG](#bookmark=id.iykjhasg1pdv)	150  
   3.   
2. RAG Corretivo: CRAG	157  
   1. Entendendo o CRAG	159  
   2. Pipeline Corretivo	162  
   3. Classe Avaliadora de Qualidade	165  
   4. Integrando a Busca Externa	171  
   5. Executando o CRAG	179

| 8 | O | RAG Adaptativo: Adaptive RAG | 182 |
| :---- | :---- | :---- | ----: |
|  | 8.1 | Visão Geral do Adaptive RAG | 183 |
|  | 8.2 | Classificador de Consultas | 186 |
|  | 8.3 | Implementando o Roteador Adaptativo | 192 |
|  | 8.4 | Executando o Adaptive RAG | 195 |

1. O RAG-Fusion	199  
   1. O Pipeline do RAG Fusion	200  
   2. A classe RAGFusion	203  
   3. Executando o Pipeline	208  
2. Hypothetical Document Embedding (HyDE)	213  
   1. O Pipeline do HyDE	214  
   2. A Classe de Geração de Documentos Hipotéticos	217  
   3. Integração com Retriever	222  
   4. Executando o HyDE	223  
   5. 

**CAPÍTULO	1**  
Gerando Revoluções

Imaginem o seguinte cenário: vocês têm um colega de classe, o Léo, que é simplesmente um gênio.  O cara leu todos os livros da biblioteca, assistiu a todas as aulas e tem uma capacidade absurda de conversar sobre qualquer assunto. Ele manja muito de história, física, arte e até daquela matéria de cálculo que todo mundo sofre. A escrita dele é fluida, convincente e ele consegue conectar ideias como ninguém. Só que o Léo tem um pequeno problema: a memória dele, apesar de vasta, às vezes prega peças. Ele pode confundir uma data, atribuir uma citação à pessoa errada ou, na pior das hipóteses, inventar um detalhe que soa verdadeiro só pra manter a conversa fluindo. Esse é o LLM puro: brilhante, mas não totalmente confiável.

Agora, vamos botar esse ’gênio’ à prova. Entreguem a ele uma prova final sobre a ’Revolução Francesa’, mas com uma pergunta bem específica: ’Qual foi o preço exato do pão em Paris na semana anterior à queda da Bastilha e como isso influenciou os discursos de Camille Desmoulins?’. O Léo, usando apenas sua memória, provavelmente vai desenrolar uma resposta incrível, bem escrita e contextualizada.  Ele vai falar sobre a fome, a crise econômica e o papel dos oradores. Mas o preço exato do pão? Ele talvez erre por alguns centavos ou invente um valor que pareça plausível. A essência da resposta estará lá, mas o dado crucial, o fato bruto, pode estar incorreto.

É aqui que a mágica do RAG começa a brilhar. Agora, imaginem que, ao lado do Léo, senta a Ana. A Ana não tem a memória enci- clopédica do Léo, mas ela é a rainha da organização e da pesquisa.

Figura 1.1: Leo e Ana. Gerador e Retriever

Ela tem um fichário perfeitamente indexado com resumos de todos os livros da biblioteca. Quando o professor faz a pergunta, antes de o Léo começar a escrever, a Ana entra em ação.  Ela não lê o livro inteiro sobre a Revolução Francesa. Ela vai direto na ficha certa, encontra o parágrafo exato sobre a economia pré-revolução e entrega ao Léo um pequeno cartão com a informação: ’Preço do pão: 4 sous. Discursos de Desmoulins mencionaram o ’preço absurdo’ como estopim para a revolta popular’. A Ana, nesse caso, é o nosso ’Retriever’.

Com esse cartão em mãos, o Léo se transforma. Ele pega aquela informação precisa e a integra em sua genialidade narrativa. A resposta dele agora não é apenas bem escrita e contextualizada, ela é factualmente irrefutável. Ele começa o texto com o dado exato, conecta o preço do pão à inflação da época e tece uma análise brilhante sobre como Desmoulins usou essa informação para inflamar a população. Ele não apenas ’colou’ a informação da Ana; ele a ’aumentou’ com seu poder de geração de texto. Essa colaboração perfeita entre o pesquisador focado (Ana) e o gerador eloquente (Léo) é a essência do ’Retrieval-Augmented Generation’.

Pensem nessa dinâmica em escala. A ’biblioteca’ não é apenas sobre a Revolução Francesa, mas sim sobre todos os documentos da sua empresa, todos os artigos médicos publicados nos últimos 20 anos, toda a base de conhecimento de um produto ou todos os

livros do Sandeco. O fichário da Ana é o nosso banco de vetores, e a habilidade dela de encontrar a ficha certa é o algoritmo de busca. Parâmetros como **chunk\_size** definem o tamanho de cada ’resumo’ no fichário dela, enquanto **top\_k** determina quantos ’cartões’ de informação ela entrega ao Léo para cada pergunta. Ajustar esses detalhes é o que transforma uma boa resposta em uma resposta perfeita.

**1.1 QUANDO USAR RAG**

A decisão de usar RAG em vez de outras técnicas, como o Fine- Tuning, não é apenas uma escolha técnica, mas uma decisão estra- tégica. Ambas as abordagens buscam especializar um LLM em um domínio de conhecimento, mas o fazem de maneiras fundamental- mente diferentes e com implicações radicalmente distintas em custo, agilidade e manutenção. Entender quando o RAG brilha é o primeiro passo para construir sistemas de IA robustos e eficientes.

O cenário ideal para o RAG é aquele onde a **verdade é volátil**. Pensem em qualquer base de conhecimento que não seja estática. A legislação de um país, por exemplo, está em constante fluxo: novas leis são sancionadas, decretos são publicados e artigos são alterados. Um sistema de IA para advogados que foi treinado ou mesmo ’fi	em um Vade Mecum de 2023 se tornaria obsoleto e perigosamente impreciso em 2024\. O custo para retreinar ou refinar o modelo a cada nova portaria seria proibitivo. O RAG resolve isso com uma elegância impressionante. A ’inteligência’ do modelo (sua capacidade de ler e interpretar) é separada do ’conhecimento’ (os documentos). Quando uma lei muda, você não toca no cérebro do LLM; você simplesmente atualiza o arquivo de texto correspondente no seu Vector Store. A verdade é atualizada em segundos, a um custo marginal.

Isso nos leva ao segundo ponto crucial: **custo e complexidade**. O Fine-Tuning, por mais poderoso que seja para alterar o ’compor- tamento’ ou o ’estilo’ de um modelo, é um processo computacional-

mente intensivo.  Ele exige a preparação de datasets massivos de exemplos, um poder de processamento considerável (geralmente múltiplas GPUs de ponta rodando por horas ou dias) e um conheci- mento técnico aprofundado para ajustar os hiperparâmetros e evitar problemas como o ’catastrophic forgetting’. É como reformar a funda- ção de um prédio. O RAG, em comparação, é como mobiliar o prédio. A implementação consiste em ’plugar’ componentes: um carregador de documentos, um modelo de embedding e um banco de vetores. A atualização do conhecimento é uma simples operação de escrita em um banco de dados, algo trivial em termos de custo computacional.

Portanto, a regra geral é clara: se o seu desafio é injetar conheci- mento factual, específico e, principalmente, **mutável** em um LLM, o RAG é quase sempre a resposta correta. Ele oferece um caminho mais barato, rápido e sustentável para manter sua IA aterrada nos fatos e sincronizada com a realidade do seu domínio de negócio.

**1.2 DECODIFICANDO A ARQUITETURA: OS BASTIDORES DO RAG**

A historinha do Léo e da Ana foi legal, né? Ajudou a dar uma clareada nas ideias. Mas agora vamos tirar os apelidos e colocar os nomes técnicos na mesa. O nosso gênio Léo é o que chamamos de **Generator**, geralmente um Modelo de Linguagem (LLM). A nossa pesquisadora supereficiente Ana é o **Retriever**. A colaboração entre eles forma o **sistema RAG**, e esse processo todo tem dois grandes momentos: uma fase de preparação, que acontece antes mesmo de vocês fazerem qualquer pergunta, e uma fase de execução, que rola em tempo real.

**Fase 1: A Preparação (Indexação de Conhecimento)**

Pensem na Ana montando o fichário dela. Isso não acontece na hora da prova, no desespero. Ela faz antes, com calma e método. No RAG, esse rolê se chama **Indexação**. É aqui que a gente pega uma

montanha de informação desestruturada e a organiza de uma forma que o nosso sistema consiga ’pesquisar’ de maneira inteligente. A gente basicamente cria o cérebro externo do nosso LLM.

O primeiro passo é **carregar os documentos**. Esqueçam livros físicos; pensem em arquivos PDF, páginas de um site, documentos de texto, transcrições de vídeos, o que for. Depois de carregar tudo, a gente precisa **quebrar esses documentos em pedaços menores**. A gente chama esses pedaços de ’chunks’. Por que fazemos isso? Simples. Mandar um livro de 500 páginas para o LLM analisar e encontrar uma única frase é ineficiente e caro. É muito mais inteligente entregar só o parágrafo certo. Aqui, vocês já encontram dois parâmetros cruciais: o **chunk\_size**, que define o tamanho de cada pedaço de texto, e o **chunk\_overlap**, que é uma pequena sobreposição entre os ’chunks’ pra garantir que a gente não perca o contexto de uma ideia que começa no final de um pedaço e termina no início do outro. Sacaram?

**Criando os mapas**

Pensem no universo de todas as ideias como uma galáxia gigante e escura. Cada ’chunk’ de texto que vocês criaram, cada conceito, é uma estrela brilhando nessa imensidão. Sozinho, é apenas um ponto de luz. O que o modelo de **Embedding** faz é atuar como um astrônomo superavançado, equipado com um telescópio que enxerga o significado.

Ele não apenas vê as estrelas; ele cria um mapa tridimensional (na verdade, com centenas de dimensões) dessa galáxia. Para cada

estrela, ou seja, para cada ’chunk’ de texto, ele atribui um conjunto de coordenadas matemáticas únicas e superprecisas. Essa lista de coordenadas **é o vetor de embedding**.

E aqui vem a parte genial, a mágica do mapa: ele não é aleatório. O nosso astrônomo (o modelo) posiciona as estrelas de forma que aquelas com ’brilho’ ou ’energia’ conceitual parecida fiquem próximas. A estrela que representa o texto ’O rei governa seu reino’ não vai estar perto da estrela ’Receita de bolo de chocolate’. Mas ela vai estar muito próxima das estrelas ’A rainha usa sua coroa’ e ’O príncipe mora no palácio’. Elas formam uma **’constelação de significado’**.

Quando vocês fazem uma pergunta, ela também é transformada em uma nova estrela, com suas próprias coordenadas, e colocada nesse mapa. A busca, então, se torna uma tarefa simples: o sistema apenas precisa olhar para a estrela da sua pergunta e identificar quais são as estrelas vizinhas mais próximas. É por isso que a busca é tão poderosa: ela não procura por palavras-chave, ela procura por **vizinhanças de significado** na galáxia das suas informações.

Com os textos todos fatiados, o próximo passo é traduzir esses ’chunks’ para uma língua que o computador entende de verdade: números. Esse processo, que é o coração da busca inteligente, se chama **Embedding**. Um modelo de ’embedding’ — pensem nele como um tradutor universal de conceitos — pega cada ’chunk’ de texto e o converte em um vetor, que é basicamente uma lista gigante

de números. A grande mágica é que textos com significados pare- cidos terão vetores (listas de números) matematicamente próximos. É como dar um CEP superpreciso para cada ideia contida nos seus documentos.

E onde a gente guarda todos esses ’CEPs’ de ideias? Num lugar especial chamado **Vector Store**, ou banco de dados de vetores. Pensem nele como o armário de fichas da Ana, mas digital, super- rápido e otimizado para buscar por proximidade. Em vez de procurar por uma palavra-chave exata, a gente entrega o ’CEP’ (vetor) da nossa pergunta e ele nos devolve os ’CEPs’ mais parecidos que ele tem guardado em questão de milissegundos. É a base da nossa busca semântica.

**Fase 2: A Execução (Recuperação e Geração)**

Certo, o fichário está pronto e organizado. Agora é hora da prova, o momento em que vocês, usuários, entram em cena. Quando vocês mandam uma pergunta, o sistema inicia a fase de **Recuperação e Geração**. A primeira coisa que ele faz é pegar a pergunta de vocês

* ’Qual foi o preço do pão em Paris?’ — e usar o **mesmo modelo de embedding** da fase anterior para transformá-la em um vetor. É fundamental que seja o mesmo modelo para que a ’linguagem’ dos CEPs seja a mesma.

  Com o vetor da pergunta em mãos, o sistema vai até o Vector Store e faz a busca por similaridade. Ele basicamente pergunta: ’Ei, me devolva os **top\_k** vetores mais parecidos com este aqui que eu te entreguei’. O parâmetro **top\_k** é simplesmente o número de ’chunks’ que vocês acham relevante recuperar. Se definirem **top\_k** como 5, ele vai pegar os 5 pedaços de texto mais relevantes da sua base de dados para responder àquela pergunta específica.

  Esses ’chunks’ recuperados são o nosso **contexto**. Agora vem o pulo do gato: o sistema monta um novo prompt, muito mais poderoso, para o LLM. Ele junta a pergunta original de vocês com o contexto que acabou de encontrar. A instrução para o LLM (o nosso Léo) é




mais ou menos assim: ’Responda à pergunta *’Qual foi o preço do pão em Paris?’* usando **apenas** as informações contidas nos seguintes textos: *\[Chunk 1, Chunk 2, Chunk 3...\]* ’. Ao forçar o LLM a se basear no contexto fornecido, a gente reduz drasticamente a chance de ele inventar coisas, ou como chamamos na área, de ’alucinar’.

E aí está. O LLM, que já é um mestre em interpretar e gerar texto, recebe a pergunta junto com a ’cola’ perfeita e factual. A tarefa dele agora não é mais ’lembrar’ a resposta, mas sim sintetizar as informações que ele acabou de receber e formular uma resposta coesa, precisa e diretamente baseada nas suas fontes. Entenderam a jogada? O RAG não deixa o LLM mais ’inteligente’ no sentido de conhecimento próprio. Ele o torna perfeitamente ’informado’ no mo- mento exato da pergunta. E é esse superpoder que vamos aprender a construir e a refinar ao longo deste livro.

**1.3 UM RAG SIMPLES**

Esta é a forma mais pura e fundamental da nossa arquitetura, o alicerce sobre o qual todas as outras variações são construídas. Pense no RAG Simples, ou ’Vanilla RAG’, como o fluxo direto que desenhamos na nossa analogia inicial. É a implementação canônica da colaboração entre o pesquisador focado (o Retriever) e o escritor eloquente (o Generator).

O processo é linear e elegante na sua simplicidade. Tudo co- meça com a pergunta do usuário. Essa pergunta é transformada em um vetor de embedding e usada para consultar o nosso banco de vetores. O banco, por sua vez, retorna os ’chunks’ de texto mais relevantes que ele possui armazenados. Estes ’chunks’ são o nosso contexto. A partir daí, a mágica acontece: a pergunta original e o contexto recuperado são combinados em um novo prompt, que é então enviado ao LLM.

A instrução para o LLM é clara e direta: "Responda a esta per- gunta usando estritamente as informações fornecidas neste contexto".

O LLM não precisa ’lembrar’ de nada do seu treinamento massivo; sua única tarefa é sintetizar, extrair e articular uma resposta a partir do material factual que acabou de receber. Não há loops, não há autocorreção, não há memória de conversas passadas. É um sis- tema de ’input-processamento-output’ direto, focado em uma única coisa: responder a uma pergunta de cada vez com a maior fidelidade possível às fontes fornecidas. Dominar este fluxo é a chave, pois cada técnica avançada que exploraremos a seguir nada mais é do que uma adição inteligente ou uma modificação engenhosa neste processo fundamental.

**1.4 ELE PODE LEMBRAR, RAG COM MEMÓRIA**

O RAG Simples que acabamos de ver é poderoso, mas tem a memória de um peixinho dourado. Ele trata cada pergunta que você faz como se fosse a primeira vez que vocês conversam. Se você perguntar ’Quem foi Santos Dumont?’ e depois ’E onde ele nasceu?’, um RAG Simples ficaria perdido. Ele não saberia a quem ’ele’ se refere. Para construir chatbots e assistentes verdadeiramente úteis, precisamos superar essa amnésia. É aqui que entra o **RAG com Memória**.

A ideia é exatamente o que o nome sugere: dar ao nosso sis- tema a capacidade de **lembrar do que foi dito antes**. Em vez de descartar a conversa após cada resposta, o sistema passa a manter um histórico do diálogo, uma espécie de ’buffer de memória’. Esse histórico se torna uma nova fonte de contexto, tão importante quanto os documentos da nossa base de conhecimento.

Na prática, isso geralmente se manifesta de uma forma muito inteligente. Quando uma nova pergunta chega — como ’E onde ele nasceu?’ — o sistema não a envia diretamente para o processo de busca. Primeiro, ele olha para a nova pergunta **e** para o histórico da conversa. Com essas duas informações, um LLM intermediário rees- creve a pergunta para que ela se torne autossuficiente. O sistema transforma a pergunta ambígua ’E onde ele nasceu?’ na pergunta

clara e completa: ’Onde Santos Dumont nasceu?’.

É essa pergunta reescrita, agora cheia de contexto, que é usada para fazer a busca no Vector Store. O resultado é uma mudança transformadora na experiência do usuário. A interação deixa de ser uma série de perguntas e respostas isoladas e se torna um diálogo fluido e natural. O sistema entende pronomes, resolve ambiguidades e permite que o usuário explore um tópico de forma orgânica. É o primeiro grande passo para transformar nosso sistema de busca em um verdadeiro parceiro conversacional.

**1.5 O RAG AUTÔNOMO: AGENT RAG**

Se o RAG com Memória deu ao nosso sistema a capacidade de lembrar, o **Agent RAG** o eleva a um novo patamar: o da autonomia e da tomada de decisão. Em vez de seguir uma sequência fixa de passos (buscar e depois gerar), um Agent RAG se comporta como um pequeno ’cérebro’ que **decide dinamicamente qual a melhor ação a tomar** para responder a uma pergunta.

Imaginem um investigador. Quando ele recebe uma pergunta complexa, ele não sai buscando em todos os arquivos de uma vez. Ele pensa: "Preciso de mais informações? Qual ferramenta devo usar? Devo consultar o banco de dados interno ou preciso pes- quisar na internet? Devo quebrar essa pergunta grande em outras menores?"O Agent RAG simula esse processo de raciocínio.

No coração de um Agent RAG está um LLM que atua como o ’agente’ principal, munido de uma lista de **ferramentas**. Essas ferramentas podem ser diversas:

* Uma ferramenta de busca no seu Vector Store (o nosso Retriever padrão).  
  * Uma ferramenta para fazer buscas na web (como uma API do Google Search).  
  * Uma ferramenta para executar código ou cálculos.  
  * Uma ferramenta para consultar uma base de dados estruturada.  
  * 

* E até mesmo ferramentas para interagir com o usuário e pedir mais esclarecimentos.  
  Quando o agente recebe uma pergunta, ele analisa o seu pedido e o seu histórico de conversa. Com base nisso, ele **decide qual ferramenta usar, se é que precisa usar alguma**. Ele pode decidir que a pergunta é simples e que ele já tem a resposta. Ou, pode concluir que precisa buscar informações em um documento especí- fico, ou que a busca na web é mais apropriada. Depois de usar uma ferramenta, o resultado é enviado de volta para o agente, que avalia se a informação é suficiente ou se ele precisa usar outra ferramenta, ou talvez refinar a busca.  
  Essa capacidade de planejar, executar e iterar nas suas próprias ações transforma o RAG de um sistema reativo em um sistema proativo. O Agent RAG pode navegar por problemas complexos, consultando diferentes fontes de informação e até mesmo corrigindo seu próprio curso. É um passo crucial em direção a IAs mais inte- ligentes e capazes de resolver problemas do mundo real de forma mais independente.

**1.6 O RAG CORRETIVO: CRAG**

No mundo real, nem toda informação é ouro. Às vezes, o nosso ’Retriever’ (o buscador de informações) pode trazer documentos irrelevantes, desatualizados ou até mesmo incorretos. Isso pode levar o LLM a gerar respostas ruins ou, o que é pior, a alucinar com base em um contexto falho. É para combater esse problema crítico que surge o **CRAG (Corrective RAG)**.

Pense no CRAG como um rigoroso editor de jornal que, antes de publicar uma matéria, verifica a qualidade das fontes. Ele não confia cegamente no que o repórter (o Retriever) trouxe. Ele adiciona uma camada inteligente de **autoavaliação e correção** à pipeline do RAG, garantindo que o LLM só receba informações de alta qualidade.

A principal inovação do CRAG reside em sua capacidade de

**avaliar a pertinência e a qualidade dos documentos recuperados**. Pesquisas recentes na área de RAG, incluindo o artigo original que propôs o CRAG, destacam que a qualidade da recuperação é o gargalo mais comum para a performance. Um CRAG faz o seguinte:

1. Após o Retriever buscar os documentos iniciais, um módulo de **avaliador de qualidade** (geralmente um LLM menor ou um modelo treinado especificamente para essa tarefa) entra em ação.  
2. Este avaliador analisa os ’chunks’ recuperados e atribui uma ’pontuação de relevância’ ou ’confi	Ele pode classificar os documentos como "altamente relevantes", "parcialmente relevan- tes"ou "irrelevantes".  
3. Com base nessa avaliação, o CRAG toma uma decisão:  
   * Se os documentos são **altamente relevantes**: Maravilha Eles são enviados diretamente para o LLM gerador.  
   * Se os documentos são **parcialmente relevantes**: O sistema pode decidir que precisa de mais informações. Ele pode, por exemplo, **expandir a busca** para documentos relacionados ou até mesmo fazer uma **nova busca na web** para encontrar informações complementares.  
   * Se os documentos são **irrelevantes**: O sistema pode optar por **descartá-los** e, talvez, tentar uma abordagem diferente de busca, ou até mesmo indicar que não conseguiu encontrar informações confiáveis.  
     Essa capacidade de ’corrigir o curso’ da recuperação é o que torna o CRAG tão poderoso. Ele não apenas busca, ele **verifica a validade da busca** e age proativamente para melhorar a qualidade do contexto antes que a geração aconteça. Isso resulta em respostas significativamente mais precisas, com menor taxa de alucinação e uma confiança muito maior na informação final apresentada ao usuário. O CRAG é um passo fundamental para tornar os sistemas RAG mais robustos e confiáveis em ambientes de dados dinâmicos e heterogêneos.  
     

**1.7 O RAG ADAPTATIVO: ADAPTIVE RAG**

A realidade é que nem toda pergunta é criada da mesma forma. Algumas são simples e diretas ("Qual a capital da França?"), en- quanto outras são complexas e exigem uma investigação profunda ("Quais foram as implicações econômicas do Tratado de Versalhes para a indústria têxtil alemã?"). Um RAG Simples trata ambas da mesma maneira: busca, concatena e gera. Isso pode ser ineficiente e até prejudicial. Para perguntas simples, a busca pode ser um des- perdício de tempo e recursos. Para perguntas complexas, uma única busca pode ser insuficiente. O **Adaptive RAG** resolve isso com uma dose de bom senso computacional.

O Adaptive RAG, como o próprio nome diz, **adapta sua estratégia com base na complexidade da pergunta**. Em vez de seguir um caminho único e rígido, ele primeiro analisa a pergunta e decide qual a rota mais eficiente para chegar à melhor resposta. Pense nele como um triagista experiente em um hospital: ele avalia o paciente (a pergunta) e o direciona para o tratamento correto, seja um curativo rápido ou uma cirurgia complexa.

O fluxo de trabalho geralmente envolve um componente inicial, um ’classifi	ou ’roteador’, que examina a pergunta do usuário. Com base nessa análise, o sistema pode decidir por um de vários caminhos:

* **Sem Busca (No Retrieval):** Para perguntas de conhecimento geral ou conversas informais ("Como você está hoje?"), o sistema pode concluir que o LLM já sabe a resposta e não precisa de busca externa. Isso economiza tempo e poder computacional.  
  * **Busca Simples (Single-step Retrieval):** Para a maioria das perguntas factuais, o sistema realiza o nosso processo RAG padrão: uma única busca no banco de vetores para encontrar o contexto relevante.

  * ## **Busca Iterativa ou em Múltiplos Passos (Multi-step Retrieval):**

Para perguntas complexas, o sistema pode iniciar um ciclo de

busca e raciocínio. Ele pode fazer uma busca inicial, analisar os resultados e decidir que precisa refinar a pergunta e buscar novamente, ou talvez decompor a pergunta original em sub- perguntas e buscar as respostas para cada uma delas antes de sintetizar a resposta final.

Essa capacidade de ajustar o esforço à complexidade da tarefa é o que torna o Adaptive RAG tão eficiente. Ele não desperdiça recursos em problemas fáceis e, ao mesmo tempo, tem a capacidade de aprofundar a investigação quando o desafio exige. É um sistema que não apenas responde, mas primeiro ’pensa’ sobre a melhor forma de responder, trazendo um nível de inteligência e otimização muito mais próximo do raciocínio humano.

**1.8 O RAG EM GRAFOS: GRAPHRAG**

Até agora, nossa visão do RAG tem sido centrada em documentos: artigos, relatórios, páginas da web. Nós quebramos esses textos em pedaços e buscamos os mais relevantes. Mas e se a informação mais valiosa não estiver contida em um parágrafo, mas sim na **relação** entre diferentes pedaços de informação? É para desvendar esse conhecimento conectado que surge o **GraphRAG**.

O GraphRAG troca a nossa tradicional base de dados de vetores por uma estrutura muito mais rica: um **Grafo de Conhecimento (Knowledge Graph)**. Pense em um grafo como um mapa de relacio- namentos. Em vez de ’chunks’ de texto isolados, temos:

* **Nós (Nodes):** Que representam entidades como pessoas, em- presas, lugares ou conceitos (ex: "Santos Dumont", "Paris", "Avião 14-Bis").  
  * **Arestas (Edges):** Que representam a relação entre essas en- tidades (ex: "Santos Dumont"*nasceu em* "Palmira", "Santos Dumont"*inventou o* "Avião 14-Bis").  
    Quando uma pergunta chega a um sistema GraphRAG, a abor- dagem é completamente diferente. Em vez de simplesmente buscar  
    

por similaridade semântica em textos, o sistema primeiro tenta enten- der as entidades e as relações na pergunta. Ele então traduz essa pergunta em uma consulta que **navega pelo grafo**.

Imagine a pergunta: "Quais inventores brasileiros moraram na mesma cidade que o criador do 14-Bis?". Um RAG tradicional teria muita dificuldade. Ele poderia encontrar documentos sobre inven- tores e sobre o 14-Bis, mas conectar os pontos seria um desafio. O GraphRAG, por outro lado, executaria uma sequência de passos lógicos:

1. Identifica que o "criador do 14-Bis"é o nó "Santos Dumont".  
2. Segue a aresta *morou em* a partir do nó "Santos Dumont"para encontrar o nó "Paris".  
3. Busca por outros nós com a propriedade *é um* "Inventor Brasi- leiro"que também tenham uma aresta *morou em* apontando para "Paris".

   O resultado é uma resposta precisa, inferida a partir das co- nexões explícitas no conhecimento. O GraphRAG é uma técnica poderosa para domínios onde as relações são a chave, como em in- vestigações financeiras (seguindo o dinheiro), descobertas científicas (conectando pesquisadores a artigos e a descobertas) e sistemas de recomendação inteligentes. Ele nos permite fazer um tipo de pergunta totalmente novo: não apenas "o quê?", mas principalmente "como se conecta?".

**1.9 O RAG HÍBRIDO: HYBRID RAG**

O **Hybrid RAG** surge como uma evolução natural quando perce- bemos que nenhum único mecanismo de recuperação é suficiente para lidar com a diversidade das perguntas do mundo real. Até agora, exploramos diferentes sabores de RAG: o baseado em vetores, o baseado em memória, RAG por Agentes e o em grafos. Mas a per- gunta é direta: por que escolher apenas um, se podemos combinar vários e tirar o melhor de cada abordagem?

Pensem no Hybrid RAG como um time multidisciplinar. Em vez de depender só da Ana (nossa Retriever clássica de vetores), trazemos também o Pedro, que é craque em grafos, e a Júlia, especialista em busca lexical. Cada um tem uma lente diferente para enxergar a informação. O segredo do Hybrid RAG está em orquestrar essas lentes para que o sistema selecione, combine ou até mesmo faça um **reranking** inteligente dos resultados.

Na prática, o Hybrid RAG combina múltiplas estratégias de recu- peração, como:

* **Busca Vetorial:** Localiza os **chunks** semanticamente mais pró- ximos da pergunta, usando embeddings.  
  * **Busca Lexical (BM25, TF-IDF):** Garante que palavras-chave exatas não passem despercebidas, algo crucial em domínios jurídicos e médicos.  
  * **Grafos de Conhecimento:** Permitem navegar em relações explí- citas, conectando conceitos que não estão no mesmo parágrafo, mas fazem parte da mesma rede de significado.  
    O desafio, claro, é decidir como combinar esses resultados. Al- guns pipelines adotam a estratégia de **união**: trazem todos os resul- tados de todas as buscas e deixam o LLM fazer a síntese. Outros preferem a **interseção**: só os documentos que aparecem em mais de um método são considerados confiáveis. A abordagem mais avançada é o **reranking neural**, onde um modelo adicional atribui pesos de relevância e reorganiza os documentos, privilegiando os mais consistentes.  
    Um detalhe importante é o papel dos hiperparâmetros. Ajustar **top\_k** em um cenário híbrido não é trivial. Pode-se definir um **top\_k** específico para cada recuperador (por exemplo, 10 vetoriais, 5 lexi- cais e 3 de grafo) ou estabelecer um limite global após o reranking. É nessa engenharia fina que o Hybrid RAG mostra sua força: a flexibilidade de moldar a recuperação ao contexto da pergunta.  
    Em resumo, o Hybrid RAG é como montar um supertime em vez de apostar todas as fichas em um único jogador. Ele reduz a chance de documentos cruciais ficarem de fora, equilibra precisão  
    

e abrangência, e garante maior robustez em domínios onde os da- dos são heterogêneos, ambíguos ou fortemente conectados. É um passo essencial para levar o RAG de uma solução pontual para uma arquitetura verdadeiramente universal e resiliente.

**1.10 O RAG-FUSION: RECIPROCAL RANK FUSION (RRF)**

O **RAG-Fusion**, também chamado de **Reciprocal Rank Fusion (RRF)**, é uma técnica refinada de combinação de resultados em bus- cas híbridas. Até agora, vimos que o Hybrid RAG mistura diferentes recuperadores (vetorial, lexical, grafos). Mas a grande pergunta é: como juntar essas listas de documentos de forma justa e eficiente? É aqui que o RRF brilha.

O truque do RRF é simples, mas genial. Imaginem duas filas de classificação: uma saída da busca vetorial e outra saída da busca lexical. Cada documento aparece em uma posição específica em cada fila (primeiro, segundo, quinto, etc.). O algoritmo RRF pega essas posições e calcula uma pontuação de relevância combinada. Quanto mais alto o documento estiver em qualquer uma das filas, maior será a sua chance de aparecer no resultado final. O efeito é equilibrar os dois mundos: semântica e palavras-chave.

O resultado é que documentos bem classificados em **qualquer um** dos métodos de busca recebem destaque. Isso é fundamental porque, em certos casos, a busca lexical pode capturar um detalhe exato (como o nome de uma lei ou artigo), enquanto a busca vetorial entende melhor o contexto semântico. O RRF garante que nenhum desses sinais seja perdido.

Na prática, o RAG-Fusion melhora muito a robustez do Hybrid RAG. Ele reduz a dependência em um único tipo de busca e cria uma fusão matemática mais estável, garantindo que documentos relevantes tenham chance real de aparecer no contexto entregue ao LLM. Além disso, como é uma técnica leve e independente do modelo, pode ser aplicada em escala, sem precisar de re-treinamento

complexo ou modelos adicionais de reranking.

Então é isso: o RAG-Fusion é como aquele juiz justo que pega notas de diferentes jurados e monta um ranking final equilibrado. Ele não deixa que a opinião de um único jurado domine o resultado, mas também não ignora quando alguém dá uma nota muito alta. Para sistemas híbridos de recuperação, o RRF é hoje uma das formas mais práticas e eficazes de combinar evidências.

**1.11 HYPOTHETICAL DOCUMENT EMBEDDING**

Um dos desafios mais sutis do RAG é o que os pesquisado- res chamam de "desalinhamento"entre a pergunta e o documento. Uma pergunta do usuário costuma ser curta, direta e usa palavras- chave específicas ("sintomas de dengue hemorrágica"). Um bom documento que responde a essa pergunta, no entanto, é geralmente longo, detalhado, usa uma linguagem mais formal e pode nem mesmo conter a frase exata da pergunta (ele pode falar de "manifestações clínicas da febre hemorrágica por dengue"). Essa diferença de estilo e conteúdo pode confundir o nosso buscador. É para resolver esse problema que existe uma técnica brilhante e um tanto contraintuitiva: o **Hypothetical Document Embedding (HyDE)**.

O HyDE parte de uma premissa genial: em vez de usar a per- gunta para encontrar uma resposta, que tal se a gente usasse uma **resposta ideal (mesmo que falsa)** para encontrar uma resposta real? É um truque mental que funciona surpreendentemente bem. O processo é o seguinte:

1. O sistema recebe a pergunta do usuário ("sintomas de dengue hemorrágica").  
2. Em vez de enviar essa pergunta direto para o banco de vetores, ele primeiro a envia para um LLM com uma instrução simples: "Escreva um documento que responda a esta pergunta".  
3. O LLM, então, gera uma **resposta hipotética**. Ele pode ’alucinar’ detalhes, mas o documento gerado será semanticamente rico,  
4. 

estruturado como uma boa resposta e conterá o vocabulário e os conceitos relevantes (ex: "O paciente pode apresentar febre alta, dor de cabeça intensa, dor retro-orbital, além de manifestações hemorrágicas como petéquias e sangramento gengival...").

5. É este documento hipotético, e não a pergunta original, que é transformado em um vetor de embedding.  
6. Finalmente, este vetor, que representa a ’essência’ de uma resposta perfeita, é usado para buscar no nosso banco de ve- tores. A busca agora não é mais "pergunta-documento", mas sim "documento-documento", o que tende a produzir resultados muito mais relevantes.

   O HyDE funciona como uma "ponte semântica". Ele traduz a intenção concisa do usuário em um exemplo detalhado do que ele espera encontrar. Mesmo que o documento hipotético contenha imprecisões, seu embedding captura o padrão geral de uma resposta relevante, tornando-o uma "isca"muito mais eficaz para "pescar"os documentos corretos na nossa base de conhecimento. É uma técnica poderosa para melhorar a precisão da recuperação, especialmente para perguntas complexas ou de nicho.

   

**CAPÍTULO	2**  
O RAG Clássico

A história do RAG Clássico começa em um momento em que os Modelos de Linguagem já mostravam seu brilho, mas também expunham suas fragilidades. Por volta de 2019 e 2020, quando os LLMs como GPT-2 e GPT-3 começaram a impressionar o mundo com textos cada vez mais coerentes e criativos, um problema ficou evidente: eles escreviam muito bem, mas não necessariamente diziam a verdade. As alucinações — respostas convincentes, porém incorretas — se tornaram um ponto crítico que limitava seu uso em cenários profissionais. Era como ter um aluno genial, mas que inventava dados quando não sabia a resposta.

Nesse cenário, surgiu a ideia de conectar esses modelos não apenas à sua memória interna, mas também a fontes externas de informação. Se o modelo é ótimo em linguagem, mas fraco em lembrança factual, por que não deixá-lo buscar os fatos em bases confiáveis antes de escrever a resposta? Esse raciocínio deu origem ao que hoje chamamos de **Retrieval-Augmented Generation**. Em vez de treinar o modelo continuamente com novos dados, que é caro e lento, a solução foi ensiná-lo a consultar documentos já disponí- veis. É aqui que nasce o RAG Clássico, a primeira arquitetura que formalizou essa fusão entre busca e geração.

O RAG Clássico foi apresentado em 2020 em um artigo da Meta AI (na época, Facebook AI Research). A proposta era direta, mas poderosa: quando o usuário fazia uma pergunta, o sistema primeiro a convertia em uma representação vetorial e consultava uma base de documentos para recuperar trechos relevantes.  Esses trechos

eram, então, combinados com a pergunta original e enviados ao LLM, que gerava a resposta fundamentada. Essa simples mudança de fluxo reduziu drasticamente as alucinações e deu origem a uma nova geração de sistemas de IA mais confiáveis.

**O link do artigo da Meta está aqui:**

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

A importância do RAG Clássico não está apenas em resolver o problema das alucinações, mas em inaugurar um novo paradigma de arquitetura. Ele mostrou que os modelos de linguagem não precisavam carregar todo o conhecimento do mundo dentro de si. Em vez disso, poderiam ser especialistas em interpretação e escrita, enquanto delegavam a tarefa de lembrança a um mecanismo externo de recuperação. Essa separação de funções foi revolucionária porque abriu caminho para IAs atualizáveis em tempo real: bastava adicionar novos documentos ao repositório, sem retreinar o modelo inteiro.

Outro impacto decisivo do RAG Clássico foi econômico. Treinar ou refinar LLMs gigantes sempre exigiu poder computacional massivo e datasets cuidadosamente preparados. O RAG Clássico quebrou essa barreira ao demonstrar que era possível manter um modelo base estático e barato, adicionando conhecimento factual de forma incremental e sob demanda. Isso reduziu custos, acelerou implemen- tações e permitiu que empresas menores também explorassem o poder dos LLMs sem precisar de uma infraestrutura bilionária.

Por fim, o RAG Clássico se consolidou como uma peça funda- mental porque trouxe confiabilidade ao centro da conversa sobre IA. Ele mostrou que a genialidade linguística dos LLMs, combinada com a precisão de bases externas, poderia produzir respostas úteis, audi- táveis e atualizadas. Em outras palavras, transformou os modelos de linguagem de curiosidades acadêmicas em ferramentas práticas para negócios, saúde, direito, jornalismo e muito mais. Esse é o legado do RAG Clássico: o ponto de partida de uma revolução que ainda está se desdobrando diante de nós.

**2.1 O QUE É UM CORPUS DE TEXTOS**

Quando falamos de RAG, uma palavra aparece o tempo todo: **corpus**. Mas afinal, o que isso significa? Um corpus de textos nada mais é do que uma coleção organizada de documentos que serve como base de conhecimento para o sistema. Esses documentos podem assumir muitas formas: artigos científicos, decisões jurídicas, páginas da web, transcrições de aulas, manuais técnicos ou até mesmo postagens em redes sociais.

O ponto central é que o corpus funciona como a **biblioteca ex- terna** do nosso modelo. Em vez de depender apenas da memória interna do LLM, o sistema consulta essa biblioteca sempre que pre- cisa de informações atualizadas ou especializadas.  Quanto mais bem estruturado for o corpus, melhor será a qualidade das respostas.

Vale lembrar que um corpus não precisa ser estático. Ele pode crescer com o tempo, receber novas versões de documentos e até ser segmentado em áreas temáticas. Essa flexibilidade é o que torna o RAG tão poderoso: basta atualizar o corpus e, automaticamente, o modelo passa a trabalhar com conhecimento mais fresco e confiável.

**2.2 O FLUXO DO RAG**

O fluxo do RAG pode ser entendido como uma sequência de etapas bem definidas que conectam a preparação dos documentos à geração final da resposta. A Figura [2.1](#bookmark=id.tonv9xmd3bd4) mostra de maneira clara como esse processo se organiza em duas grandes fases: a fase de **Indexing**, que ocorre de forma offline, e a fase online do próprio RAG, acionada a cada consulta do usuário.

Na parte superior da imagem, vemos a fase de **Indexing**. É aqui que o **corpus**, isto é, o conjunto de documentos brutos, passa por um **Preprocess**, onde o texto é limpo e normalizado. Em seguida, o material é segmentado em pedaços menores por meio do **Chunking**, o que facilita a manipulação e garante granularidade na hora da busca. Esses segmentos, então, são convertidos em vetores pelo módulo de **Embedding**, e finalmente armazenados em um **Vector Database**. Esse banco é a estrutura que permite que, no futuro, as consultas sejam respondidas de forma rápida e precisa.

Na parte inferior da Figura [2.1,](#bookmark=id.tonv9xmd3bd4) está a fase online, isto é, o mo- mento em que o usuário faz sua pergunta. A **Query** é recebida e imediatamente transformada em um embedding, permitindo que fale a mesma língua matemática dos documentos armazenados. Esse vetor da consulta é enviado ao **Retriever**, que consulta o Vector Database e devolve os **chunks** mais relevantes. Na sequência, entra em cena o **Augmented**, que combina a pergunta original com os trechos recuperados, criando um prompt enriquecido. Esse prompt é passado ao módulo de **Generation**, onde o LLM produz a resposta final, agora fundamentada em dados concretos.

Não se preocupe se algum desses termos ainda parece abstrato. Ao longo das próximas seções, vamos destrinchar cada parte do fluxo separadamente — explicando com calma o que é o **Retriever**, o que significa **Augmented**, como funciona a **Generation** — e mais: você vai implementar em Python cada uma dessas etapas para ver o RAG ganhar vida em código.

Figura 2.1: O fluxo do RAG Clássico dividido em duas fases: Indexing (offline) e execução do RAG (online).

**2.3 A FASE DO INDEXADOR**

Imagine uma grande biblioteca que acabou de receber milhares de novos livros. Antes que os leitores possam consultar esse acervo, é necessário que bibliotecários os organizem: cataloguem títulos, autores, assuntos e os coloquem nas prateleiras corretas. Sem esse trabalho de bastidores, encontrar qualquer informação se tornaria uma tarefa caótica e lenta. No RAG, essa função de organização e preparação é realizada pelo **Indexador**.

O Indexador é a etapa responsável por transformar o **corpus** bruto em uma estrutura que possa ser consultada de forma eficiente pelo sistema. Ele começa recebendo os documentos originais, que podem ser artigos, decisões jurídicas, relatórios técnicos ou até postagens em redes sociais.

Em seguida, o Indexador divide os documentos em pedaços menores, chamados de **chunks**. Essa segmentação é essencial porque evita que o sistema tenha que lidar com textos enormes e dispersos. Ao trabalhar com trechos curtos, a busca se torna mais precisa e o risco de perder detalhes importantes diminui. Cada chunk funciona como uma ficha de catálogo, pronta para ser indexada.

Finalmente, cada chunk é convertido em um vetor de **embedding**, que representa matematicamente o seu significado. Esses vetores são armazenados em um **Vector Database**, que é o equivalente digital de um catálogo bem organizado. Quando o usuário fizer uma pergunta, o sistema não precisará ler tudo de novo: bastará consultar o índice construído pelo Indexador. É por isso que essa fase é considerada o alicerce de todo o RAG, garantindo velocidade, precisão e confiabilidade na etapa de recuperação.

**Instalando tudo**

Para começar, faça o download do nosso projeto no link abaixo:

**Link do projeto:**

[https://bit.ly/sandeco\_rag\_classico](https://bit.ly/sandeco_rag_classico)

Certifique-se de que o seu ambiente já esteja preparado com a versão mais estável do python, eu recomendo o **Python 3.12**. Além disso, instale o gerenciador de pacotes **UV**, que será utilizado para configurar as dependências do projeto. Para instalar o UV, execute o seguinte comando no terminal:

**pip install uv**

Com o UV instalado, crie um ambiente virtual já apontando para a versão correta do Python e depois sincronize todas as dependências do projeto com os comandos abaixo:

**uv venv \--python=3.12 uv sync**

**2.4 LENDO E CONVERTENDO**

A primeira tarefa da indexação é a abertura, leitura e transfor- mação dos documentos em um formato que possa ser manipulado pelo sistema. Por isso, criamos a classe **ReadFiles**. Observe que, ao inicializar essa classe, nenhuma configuração especial é feita no método init  . O foco está em disponibilizar um ponto de entrada para os métodos que realmente executam o processamento. O mé- todo central se chama **docs\_to\_markdown**, e é nele que acontece o fluxo completo: receber um diretório, identificar os arquivos dentro dele, converter cada um para markdown e salvar o resultado.

No início do método **docs\_to\_markdown**, a lista de arquivos é capturada com a função **read\_dir**, que retorna todos os nomes exis- tentes no diretório passado. Para cada arquivo, construa o caminho completo com **os.path.join**. Em seguida, determine a extensão com

o comando **file.split(’.’)\[-1\]**, que pega exatamente o que está após o último ponto no nome. Esse detalhe é importante porque arquivos como 2111.01888v1.pdf têm mais de um ponto no nome. O split garante que só a última extensão seja considerada para identificar o tipo.

Se o arquivo for de texto ou documento, como pdf, docx, csv ou similares, crie um objeto **MarkItDown** com plugins habilitados. Caso o arquivo seja uma imagem, inicialize o **MarkItDown** com parâmetros diferentes: passe um cliente **OpenAI**, defina o modelo gpt-5-mini e um prompt que instrui o sistema a gerar três parágrafos descrevendo a imagem em português. Essa distinção mostra que o tratamento varia de acordo com o tipo de dado: texto estruturado segue direto para a conversão, enquanto imagens exigem interpretação por meio de linguagem natural.

Depois de converter o arquivo com **md.convert**, salve o resultado em formato markdown dentro da pasta markdown. Para isso, use **os.path.splitext** para remover a última extensão e criar um nome limpo, adicionando .md ao final. Se a pasta não existir, crie-a com **os.makedirs**. Por fim, abra o arquivo resultante em modo de escrita com codificação utf-8 e grave o conteúdo. Quando todos os arqui- vos já foram processados, percorra novamente a pasta markdown, leia cada documento salvo e concatene em uma única string, que é devolvida pelo método. Esse comportamento garante que o resultado final da indexação esteja pronto para ser usado na próxima etapa do RAG.

**\#read\_files.py**

**import os**

**from markitdown import MarkItDown**

**class ReadFiles:**

**def**	**init**	**(self): pass**

**def docs\_to\_markdown(self, dir\_path): docs \= self.read\_dir(dir\_path) for file in docs:**

**file)**

 **file\_path \= os.path.join(dir\_path,**

| extension | \== | ’doc’ or \\ |
| :---- | :---- | :---- |
| **extension** | **\==** | **’docx’ or \\** |
| **extension** | **\==** | **"xls" or \\** |
| **extension** | **\==** | **"xlsx" or \\** |
| **extension** | **\==** | **"ppt" or \\** |
| **extension** | **\==** | **"pptx" or \\** |
| **extension** | **\==** | **"csv" or \\** |
| **extension** | **\==** | **"txt" or \\** |
| **extension** | **\==** | **"json" or \\** |
| **extension** | **\==** | **"xml" or \\** |
| **extension** | **\==** | **"html" or \\** |
| **extension** | **\==** | **"htm" or \\** |
| **extension** | **\==** | **"yaml":** |

**extension \= file.split(’.’)\[-1\] if extension \== ’pdf’ or \\**

**True)**

 **md \= MarkItDown(enable\_plugins=**

**elif extension \== ’jpg’ or \\**

| extension | \== | ’png’ or \\ |
| :---- | :---- | :---- |
| **extension** | **\==** | **’jpeg’ or \\** |
| **extension** | **\==** | **’gif’ or \\** |
| **extension** | **\==** | **’bmp’ or \\** |
| **extension** | **\==** | **’webp’ or \\** |

| extension | \== | ’svg’ or \\ |
| :---- | :---- | :---- |
| **extension** | **\==** | **’tiff’ or \\** |
| **extension** | **\==** | **’ico’:** |

**client \= OpenAI()**

**mini", parágrafos,**

 **md \= MarkItDown(llm\_client=client,**  
**llm\_model="gpt-5- llm\_prompt="""Em 3**

**descreva a imagem**

**detalhadamente em**

**True)**

   
**pt-br""", enable\_plugins=**

**result \= md.convert(file\_path)**

**filename\_without\_ext \= os.path. splitext(file)\[0\]**  
**md\_path \= os.path.join("markdown",**  
**filename\_without\_ext \+ ".md")**

**if not os.path.exists("markdown"): os.makedirs("markdown")**

**with open(md\_path, "w", encoding="utf**

**\-8") as f:**  
**f.write(result.text\_content) md\_content \= ""**

**for file in os.listdir("markdown"):**

**with open(os.path.join("markdown", file), "r", encoding="utf-8") as f:**  
**md\_content \+= f.read()**

**return md\_content**

**def read\_dir(self, dir\_path): files \= os.listdir(dir\_path) return files**

**2.5 CHUNKING**

Imagine que você precisa estudar para uma prova de história, mas o livro tem 800 páginas. Se você tentar ler tudo de uma vez, ficará sobrecarregado e não vai conseguir lembrar dos detalhes importantes. A solução natural é dividir o livro em capítulos, depois em seções e, às vezes, até em resumos menores com pontos-chave. Essa é exatamente a lógica do **Chunking** no RAG: pegar documentos grandes e fragmentá-los em pedaços menores e mais fáceis de manipular.

O **Chunking** acontece logo no início do processo de indexação. Cada documento é cortado em blocos de texto — os **chunks**. Es- ses blocos têm um tamanho pré-definido, controlado pelo parâmetro **chunk\_size**. Definir bem esse tamanho é crucial: se o chunk for muito grande, o modelo pode receber informações demais e se perder no excesso de contexto; se for muito pequeno, pode faltar informação para dar sentido ao texto recuperado. Encontrar o equilí- brio é como ajustar a lente de uma câmera: nem perto demais, nem distante demais.

Outro ponto importante é o **chunk\_overlap**, que adiciona uma

pequena sobreposição entre os chunks. Pense em duas páginas consecutivas de um livro: a frase pode começar no final de uma e terminar no início da outra. Se os blocos não se sobrepuserem, esse detalhe pode ser perdido. O overlap garante que o contexto não se quebre de forma brusca, permitindo que a busca recupere informações mais completas e coerentes.

No fim das contas, o **Chunking** é o que transforma documentos extensos em uma base granular e eficiente para o RAG. Ele prepara o material de forma que cada pergunta feita pelo usuário encontre pedaços de informação relevantes, já prontos para serem buscados e usados pelo Retriever. Sem essa etapa, o sistema teria de lidar com blocos desorganizados e desproporcionais, comprometendo tanto a performance quanto a precisão da resposta.

**A Classe Chunks**

A classe **Chunks** do nosso projeto, possui métodos públicos que permitem controlar todo o processo de fragmentação de textos em pedaços menores e reutilizáveis. O método **create\_chunks(text)** recebe um texto em formato de string e o divide em blocos de acordo com o **chunk\_size** e o **overlap\_size**. Durante essa divisão, ele tenta preservar a coerência natural do conteúdo, procurando pontos adequados de corte, como quebras de parágrafo, final de frases ou espaços entre palavras. O resultado é uma lista de chunks prontos para serem usados em indexação ou busca.

## O método **create\_chunks\_with\_metadata(text, source\_info)**

vai além: além de gerar os chunks, ele também adiciona informações

extras a cada um deles. Essas informações incluem um identificador único para cada chunk, o texto em si, o tamanho do chunk, a quan- tidade total de chunks criados, a posição inicial estimada no texto original e ainda dados opcionais de **source\_info**, que podem descre- ver a origem ou outras características do documento processado. O retorno é uma lista de dicionários, cada um representando um chunk enriquecido com metadados.

O método **get\_chunk\_info()** retorna um resumo das configura- ções ativas da classe. Ele mostra o **chunk\_size**, o **overlap\_size** e o passo efetivo da divisão, calculado pela diferença entre os dois. Essa consulta é útil para validar se os parâmetros atuais estão de acordo com o esperado antes de iniciar a criação de novos chunks.

Por fim, o método **update\_settings(chunk\_size, overlap\_size)** permite atualizar dinamicamente as configurações de chunking. O usuário pode modificar tanto o tamanho dos chunks quanto a sobre- posição entre eles, e o método se encarrega de validar os novos valores, garantindo que não haja inconsistências, como uma sobrepo- sição maior que o chunk em si. Esse recurso torna a classe flexível, permitindo ajustes finos para diferentes tipos de textos ou cenários de aplicação.

**2.6 CRIAÇÃO DE EMBEDDINGS**

Ainda em organização de livros, em vez de guardar os exemplares apenas pelo título, você decide criar um mapa em que cada livro recebe coordenadas de acordo com o seu tema, estilo e vocabulário. Assim, romances parecidos ficam próximos uns dos outros, livros de física ocupam outra região e poesias formam seu próprio agrupa- mento. Essa é a essência da criação de **embeddings**: transformar textos em pontos de um espaço multidimensional onde a proximidade reflete a semelhança de significado.

No contexto do RAG, a criação de embeddings é o passo seguinte após o **chunking**. Cada **chunk** é convertido em um vetor numérico,

ou seja, uma lista de números que representa o conteúdo semân- tico daquele pedaço de texto. Essa tradução é feita por um modelo especializado de embedding, que captura padrões de linguagem e os projeta em um espaço vetorial de alta dimensionalidade. O grande benefício é que textos com sentidos parecidos acabam fi- cando matematicamente próximos uns dos outros. Esse processo de vetorização cria uma espécie de mapa conceitual que torna possível a busca semântica. Em vez de procurar apenas por palavras exatas, o sistema pode encontrar conteúdos relacionados por significado.

Por exemplo: observe as duas Figuras abaixo. Veja como os **chunks** de texto são enviados ao **Semantic Encoder**, que atua como um tradutor semântico. Faça a leitura dessa conversão como uma mudança de idioma: o que antes era linguagem natural passa a ser representado em coordenadas matemáticas chamadas de **embeddings**. Escreva mentalmente essa associação, pois ela será a base para todo o processo de busca semântica no RAG.

Esses embeddings não são palavras, mas sim posições em um espaço de significados. Quanto mais próximos estiverem dois ve- tores, mais parecidos são seus conteúdos originais. Isso significa que textos diferentes, mas semanticamente relacionados, ficam pró- ximos nesse mapa multidimensional. Fixe essa noção, porque é exatamente dessa forma que o RAG será capaz de encontrar infor- mações relevantes, não apenas pelo termo usado, mas pelo sentido carregado no contexto.

É aqui que a inteligência do RAG começa a se destacar em relação à simples busca lexical.

**SentenceTransformer**

Para gerar os **embeddings** de texto no nosso pipeline, vamos utilizar a classe SentenceTransformer, disponível na biblioteca sentence\_transformers. Essa classe encapsula modelos de lin- guagem treinados para converter sentenças, parágrafos ou docu- mentos inteiros em representações vetoriais de alta dimensionali- dade. Diferente de vetorizadores simples baseados em frequência de palavras, como TF-IDF, o **SentenceTransformer** captura nuances semânticas, garantindo que textos com significados próximos sejam

mapeados para vetores igualmente próximos no espaço vetorial.

No nosso caso, adotamos o modelo paraphrase-multilingual-MiniLM-L1

Esse modelo é multilíngue, isto é, foi treinado para lidar com dife- rentes idiomas, incluindo o português, e retorna embeddings com tamanho fixo de **384 dimensões**. Esse valor significa que cada sentença ou documento é convertido em um vetor de 384 números, posicionados em um espaço semântico multidimensional. Nesse espaço, textos com significados semelhantes ficam próximos entre si, enquanto textos de temas diferentes ficam mais distantes. Essa ca- racterística é o que permite ao RAG realizar a busca semântica com precisão. Nos próximos capítulos, exploraremos outros modelos de **SentenceTransformer**, comparando seus tamanhos de embeddings, desempenho e adequação a diferentes contextos de uso.

Antes de utilizar a classe, instale a biblioteca no ambiente do projeto com o seguinte comando:

**uv add sentence\_transformers**

Depois da instalação, vamos testar o modelo em um código simples em Python direto:

**from sentence\_transformers import**

**SentenceTransformer**  
**\# Inicializa o modelo multilíngue**

**model \= SentenceTransformer(’paraphrase- multilingual-MiniLM-L12-v2’)**  
**\# Exemplo de textos**

**sentencas \= \[**  
**’O RAG combina**

**’Os embeddings frases.’,**

**’ChromaDB é um**  
**busca e geração.’,**

**representam o significado de**  
**banco de dados vetorial.’**  
**\]**

**\# Geração dos embeddings**

**vetores \= model.encode(sentencas)**

**print(vetores.shape)	\# (3, 384\)**

**2.7 BANCO DE DADOS VETORIAL**

Depois de criados, os embeddings são armazenados no **banco de vetores**, que funciona como um catálogo digital extremamente eficiente. Esse banco permite consultas rápidas e precisas: quando uma pergunta chega, ela também é convertida em um vetor e compa- rada com os vetores já guardados. Os mais próximos são retornados como contexto relevante. Sem a criação de embeddings, não haveria como o sistema localizar informações de forma semântica; seria como tentar navegar na feira de livros sem o mapa, apenas andando às cegas.

**ChromaDB**

O **ChromaDB** é uma das implementações mais populares de banco de dados vetorial no ecossistema de RAG. Ele foi projetado para armazenar, indexar e consultar **embeddings** de forma eficiente, oferecendo suporte nativo para operações de similaridade semântica. Diferente de bancos relacionais tradicionais, o ChromaDB trabalha em um espaço de alta dimensionalidade, onde cada vetor representa um pedaço de conhecimento. Sua arquitetura otimizada permite consultas extremamente rápidas, mesmo em coleções com milhões de vetores, garantindo que o **Retriever** consiga responder em tempo hábil sem comprometer a precisão.

Outro ponto de destaque do **ChromaDB** é sua simplicidade de uso e integração com frameworks modernos. Ele suporta tanto arma- zenamento em memória quanto persistência em disco, o que facilita

experimentos locais e também projetos em produção. Além disso, disponibiliza recursos como filtros condicionais, atualizações incre- mentais de coleções e compatibilidade com diferentes formatos de embeddings. Isso torna o ChromaDB uma escolha versátil para apli- cações práticas de RAG, equilibrando desempenho, escalabilidade e facilidade de adoção no fluxo de desenvolvimento.

**2.8 NOSSA CLASSE DE ENCODER**

Agora que entendemos todas as partes da indexação, vamos criar uma classe chamada ’SentenceEncoder’ que vai ler os arquivos PDF de uma pasta, transformar os textos em chunks, transformar em embeddings e salvar no ChromaDB.

Comece analisando a primeira parte do código. Escreva as impor- tações que trazem as dependências externas e internas que serão usadas pelo restante da classe. Veja que são importados os módulos Chunks, ReadFiles, o modelo SentenceTransformer, além do chromadb e do uuid. Esses módulos permitem organizar os textos em chunks, transformar em embeddings e salvar no banco vetorial.

**\# aquivo semantic\_encoder.py**

**from chunks import Chunks**

**from read\_files import ReadFiles from sentence\_transformers import**

**SentenceTransformer import chromadb import uuid**

Na sequência, observe a definição da classe SemanticEncoder. Escreva o construtor init recebendo os parâmetros principais: o diretório dos documentos, o tamanho dos chunks, a sobreposição, o caminho do banco ChromaDB e o nome da coleção. Note que no corpo do      init     são inicializadas as dependências essenciais: a

leitura de arquivos, o chunker, o modelo de embeddings multilíngue, o cliente persistente do ChromaDB e o atributo collection.

**class SemanticEncoder: """**

**Constrói a base vetorial e popula o ChromaDB a partir de documentos em um diretório.**

**"""**

**def**	**init**	**( self, docs\_dir: str,**  
**chunk\_size: int,**  
**overlap\_size: int,**

**db\_path: str \= "./chroma\_db", collection\_name: str \= "documentos\_rag",**

**) \-\> None:**

**self.docs\_dir \= docs\_dir self.chunk\_size \= chunk\_size self.overlap\_size \= overlap\_size self.db\_path \= db\_path self.collection\_name \= collection\_name**

**\# Dependências self.rf \= ReadFiles()**  
**self.chunker \= Chunks(chunk\_size=self.**  
**chunk\_size, overlap\_size=self.overlap\_size) self.modelo \= SentenceTransformer(’**

**paraphrase-multilingual-MiniLM-L12-v2’) self.client \= chromadb.PersistentClient(**  
**path=self.db\_path)**

**self.collection \= None**

Agora concentre-se no método build. Execute cada etapa com clareza: primeiro, leia os documentos e converta-os em markdown. Depois, crie os chunks de texto e aplique o modelo para gerar os embeddings.  Observe que os embeddings são transformados em

listas porque o ChromaDB exige esse formato. Em seguida, recrie ou obtenha a coleção no banco vetorial. Se reset\_collection for True, apague a coleção existente antes de prosseguir.

**def build(self, reset\_collection: bool \= True, collection\_name: str \= None) \-\> dict:**

**\# 1\) Ler documentos**  
**mds \= self.rf.docs\_to\_markdown(self.docs\_dir)**

**\# 2\) Criar chunks**  
**text\_chunks \= self.chunker.create\_chunks(mds)**

**\# 3\) Gerar embeddings  base\_vetorial\_documentos \= self.modelo.encode(**  
**text\_chunks)**  
**embeddings \= base\_vetorial\_documentos.tolist()**

**\# 4\) (Re)criar/obter coleção if reset\_collection:**

**try:**

**self.client.delete\_collection(name= collection\_name)**  
**print(f"Coleção ’{collection\_name}’ existente foi deletada.")**

**except Exception: pass**

**try:**

**self.collection \= self.client. get\_collection(name=collection\_name)**

**except Exception:**

**self.collection \= self.client. create\_collection(**  
**name=collection\_name, metadata={"description": "Coleção de**

**chunks de documentos com embeddings"},**

**)**

Finalize entendendo a inserção dos dados no ChromaDB. Crie identificadores únicos com uuid, construa metadados com informa- ções do chunk e use o método add para inserir embeddings, docu- mentos e metadados na coleção. Por fim, imprima as estatísticas do processo e retorne um dicionário com os resultados.

**\# 5\) Inserir dados**

**ids \= \[str(uuid.uuid4()) for \_ in range(len( text\_chunks))\]**

**metadatas \= \[**

**{**

**"chunk\_id": i, "chunk\_size": len(chunk), "source": self.docs\_dir,**

**}**  
**for i, chunk in enumerate(text\_chunks)**

**\]**

**self.collection.add( ids=ids, embeddings=embeddings, documents=text\_chunks, metadatas=metadatas,**

**)**

**print(f" Salvos {len(text\_chunks)} chunks no ChromaDB\!")**

**print(**  
**f" Coleção ’{self.collection\_name}’ agora possui {self.collection.count()} documentos"**

**)**

**return {**  
**"chunks\_salvos": len(text\_chunks),**

**"colecao": self.collection\_name,**  
**"total\_documentos": self.collection.count**  
**(),**

**}**

**Criando uma main**

Por último, veja o bloco principal que é executado quando o ar-

quivo é rodado diretamente. Observe a criação do objeto SemanticEncoder

com os parâmetros de diretório, chunk e overlap. Em seguida, exe- cute o método build para construir a base vetorial e imprimir esta- tísticas.

**if**		**name**	**\== "**	**main** 	 **": encoder \= SemanticEncoder(**  
**docs\_dir="docs", \#diretório dos documentos**

**chunk\_size=2000, \#tamanho do chunk overlap\_size=500, \#tamanho da sobreposição**

**)**

**\# Construir base vetorial**

**stats \= encoder.build(collection\_name=" synthetic\_dataset\_papers")**

**\# Imprimir estatísticas print(stats)**

Depois da execução do arquivo main.py, surgem automatica- mente duas pastas fundamentais para o funcionamento do projeto. A pasta chroma\_db é responsável por armazenar o banco vetorial utili- zado nas buscas semânticas do RAG, enquanto a pasta markdown concentra os arquivos convertidos a partir dos documentos originais presentes em docs. Essa organização garante que os dados brutos fiquem separados dos conteúdos processados e que o índice vetorial

possa ser consultado de forma rápida e eficiente.

**2.9 RECUPERANDO CONHECIMENTO**

Imagine que vai alguém que vai entrar na sua biblioteca gigan- tesca com milhares de livros e, no balcão, encontrar um bibliotecário extremamente eficiente. Ele faz uma pergunta e, em vez de ler todos os volumes, esse bibliotecário sabe exatamente em quais prateleiras e páginas procurar. Ele não te entrega o livro inteiro, mas destaca apenas os trechos mais relevantes que respondem à sua dúvida. Esse bibliotecário é a perfeita analogia para o **Retriever** dentro do RAG.

O papel do Retriever é localizar no **corpus** os pedaços de texto mais próximos daquilo que foi perguntado. Para isso, ele transforma a pergunta em uma representação numérica chamada **embedding**, um vetor de números que captura o significado semântico do enunciado. Em seguida, o Retriever consulta o banco de vetores, comparando essa representação com as representações já armazenadas dos documentos. O resultado é uma lista de **chunks** que estão semanti- camente mais próximos da pergunta.

É importante perceber que o Retriever não inventa nada, ele apenas busca. A sua função é trazer para o modelo gerador a parte da informação que realmente importa. Se pensarmos novamente na analogia da biblioteca, ele não dá opiniões, não interpreta, apenas recupera. A qualidade do trabalho do Retriever depende de fatores como a escolha do modelo de embedding, o **chunk\_size** usado para dividir os documentos e o parâmetro **top\_k**, que define quantos trechos devem ser retornados.

Sem o Retriever, o RAG não teria como se apoiar em informações

externas. Ele é a ponte entre o modelo de linguagem e a base de conhecimento. É por meio dele que a resposta deixa de ser apenas uma construção da memória do LLM e passa a ser fundamentada em dados concretos. Em resumo, o Retriever é quem garante que a conversa com a máquina não seja apenas bonita, mas também informada.

**A classe de Recuperação**

Agora vamos construir o **retriever**, que será o responsável por realizar buscas semânticas na base vetorial. Observe a primeira parte do código. Escreva o cabeçalho com o nome do arquivo e faça as importações necessárias: o módulo chromadb, a classe SentenceTransformer para geração de embeddings e o módulo sys para permitir encerrar a aplicação em caso de erro.

**\# arquivo retriever.py**

**import chromadb**  
**from sentence\_transformers import SentenceTransformer**

**import sys**

Na sequência, defina a classe Retriever. Execute o método

    init passando o caminho para o banco ChromaDB e o nome da coleção. Dentro do construtor, inicialize os atributos que armazenam o cliente, a coleção e o modelo de embeddings. Em seguida, chame o método interno \_initialize() para configurar a conexão com o banco vetorial e carregar o modelo.

**class Retriever:**

**def**	**init**	**(self, db\_path="./chroma\_db", collection\_name=""):**

**"""**

**Inicializa o sistema de query RAG.**

**"""**  
**self.db\_path \= db\_path self.collection\_name \= collection\_name self.client \= None**

**self.collection \= None self.modelo \= None**

**self.\_initialize()**

Agora concentre-se no método \_initialize. Execute a cone- xão persistente com o ChromaDB utilizando o caminho configurado e recupere a coleção pelo nome fornecido. Em seguida, carregue o mo- delo de embeddings paraphrase-multilingual-MiniLM-L12-v2. Repare que há mensagens de saída informando a conexão bem- sucedida e o número de documentos na coleção. Se ocorrer algum erro, capture a exceção, informe o usuário e encerre o programa com sys.exit(1).

**def \_initialize(self):**

**"""Inicializa o cliente ChromaDB e carrega o modelo."""**

**try:**

**\# Conectar ao ChromaDB self.client \= chromadb.**  
**PersistentClient(path=self.db\_path)**

**self.collection \= self.client. get\_collection(name=self.collection\_name)**

**\# Carregar modelo de embeddings print("Carregando modelo de embeddings**

**...")**

**self.modelo \= SentenceTransformer(’ paraphrase-multilingual-MiniLM-L12-v2’)**

**print(f"Conectado à coleção ’{self. collection\_name}’")**

**print(f"Total de documentos: {self. collection.count()}")**

**except Exception as e:**

**print(f" Erro ao inicializar: {e}") print("Certifique-se de que o banco**  
**ChromaDB foi criado executando rag\_classic.py**

**primeiro.")**

**sys.exit(1)**

Por fim, veja o método search. Escreva a query em linguagem natural e transforme-a em embedding usando o modelo carregado. Depois, utilize o método query do ChromaDB para buscar documen- tos semelhantes, especificando o número de resultados e pedindo que sejam retornados documentos, distâncias e metadados. Note que o código extrai a primeira lista de documentos recuperados e a retorna como resultado da busca. Caso aconteça algum erro, capture a exceção e retorne None.

**def search(self, query\_text, n\_results=5, show\_metadata=False):**

**"""**

**Busca documentos similares à query. """**

**try:**

**\# Gerar embedding da query query\_embedding \= self.modelo.encode(\[**  
**query\_text\])**

**\# Buscar no ChromaDB**

**results \= self.collection.query( query\_embeddings=query\_embedding.**

**tolist(),**  
**n\_results=n\_results, include=\[’documents’, ’distances’,**

**’metadatas’\]**

**)**

**res \= results\[’documents’\]\[0\] return res**

**except Exception as e:**

**print(f" Erro na busca: {e}") return None**

**2.10 AUMENTO DE INFORMAÇÃO**

O **Augmented** é a etapa do RAG em que a consulta original do usuário deixa de ser tratada de forma isolada e passa a ser enriquecida com informações adicionais provenientes do **Retriever**. Em outras palavras, é aqui que o sistema pega a pergunta feita pelo usuário e a amplia com os trechos mais relevantes recuperados da base vetorial. Esse processo é chamado de **aumento de informação** porque transforma um simples enunciado em um contexto muito mais rico, capaz de guiar o modelo de linguagem a produzir respostas fundamentadas.

No nosso caso específico, o **Augmented** não envolve nenhuma arquitetura complexa, mas sim a construção de um *prompt* cuida- dosamente montado.  O que fazemos é pegar a **query** do usuário e combiná-la com os **chunks** selecionados pelo **Retriever**. Dessa forma, o modelo de linguagem não precisa inventar informações do zero: ele já recebe como entrada uma pergunta acompanhada de passagens textuais que têm grande chance de conter a resposta correta ou, pelo menos, partes essenciais dela.

Esse simples mecanismo de concatenação garante que a saída gerada esteja conectada aos documentos originais. Com isso, ao invés de depender apenas da memória estatística do modelo, forne-

cemos evidências explícitas no prompt. Esse processo fortalece a confiabilidade da resposta e reduz drasticamente o risco de alucina- ções. Portanto, o **Augmented** é a ponte que une o que foi recuperado na base vetorial com o poder de geração do modelo, dando ao RAG sua característica essencial: responder de forma criativa sem perder a ligação com os dados de origem.

A classe Augmentation é responsável por construir o **prompt** que será enviado ao modelo de linguagem. Observe que ela possui um método estático chamado generate\_prompt, que recebe dois parâmetros: a **query** do usuário e os **chunks** selecionados pelo **Re- triever**. Primeiro, defina um separador visual para organizar melhor os blocos de texto. Em seguida, formate os chunks, adicionando um cabeçalho chamado Conhecimento para indicar ao modelo que aquele conteúdo representa a base de dados disponível. Por fim, construa uma string estruturada em que o texto da consulta apa- rece delimitado por \<query\> e os chunks aparecem entre \<chunks\>. Essa formatação garante que o modelo saiba claramente o que é a pergunta e quais são as evidências textuais que deve usar na resposta. Ao retornar esse prompt, a classe entrega uma entrada enriquecida e padronizada, pronta para ser utilizada pelo RAG.

**class Augmentation:  def**	**init**	**(self):**

**pass**

**@staticmethod**  
**def generate\_prompt(query\_text, chunks):**

**separador \= "\\n\\n------------------------\\**

**n\\n"**

**\# Junta os chunks com o separador e adiciona o cabeçalho**  
**chunks\_formatados \= f"Conhecimento\\n**

**\------------------------\\n\\n{separador.join( chunks)}"**

**prompt \= f"""Responda em pt-br e em markdown, a query do usuário delimitada por \< query\>**

**usando apenas o conhecimento dos chunks delimitados por \<chunks\>.**

**Combine as informações dos chunks para responder a query de forma unificada.**

**Se por acaso**

**o conhecimento não for suficiente para responder a query, responda apenas**

**que não temos conhecimento suficiente para responder a query.**

**\<chunks\>**  
**{chunks\_formatados}**

**\</chunks\>**

**\<query\>**  
**{query\_text}**

**\</query\> """**

**return prompt**

**2.11 GERANDO A RESPOSTA**

A classe Generation funciona como um **Adapter** que encapsula a comunicação com o modelo da Google Gemini, simplificando sua utilização no fluxo do RAG. No construtor init , observe que primeiro é carregado o arquivo .env para obter a chave da API de forma segura, evitando expor informações sensíveis no código. Em seguida, a classe inicializa o cliente da API do Gemini com a chave

recuperada e define o modelo a ser utilizado, que por padrão é o gemini-2.5-flash. Dessa forma, ao instanciar a classe, todo o processo de configuração de credenciais e escolha do modelo já está resolvido, permitindo uma integração direta e transparente.

O método generate é o ponto em que a geração da resposta acontece de fato. Ele recebe o **prompt** já preparado na etapa de **Augmented** e o envia ao serviço do Gemini utilizando a função generate\_content. A resposta retornada pela API é então extra- ída e devolvida apenas como texto, pronta para ser consumido no pipeline do RAG. Esse design de Adapter é importante porque de- sacopla a lógica do RAG da implementação específica do provedor de LLM. Assim, se no futuro for necessário trocar o modelo ou até mesmo o provedor, basta modificar essa classe, mantendo o restante do código intacto.

**from google import genai**  
**from dotenv import load\_dotenv import os**

**class Generation:**

**def**	**init**	**(self, model="gemini-2.5-flash"): load\_dotenv()**  
**self.client \= genai.Client(api\_key=os. getenv("GEMINI\_API\_KEY"))**

**self.model \= model**

**def generate(self, prompt): client \= genai.Client()**  
**response \= client.models.generate\_content(**

**model=self.model, contents=prompt,**

**)**

**return response.text**

**2.12 RODANDO COM STREAMLIT**

O código abaixo representa a junção de todas as etapas do RAG: **Retriever**, **Augmented** e **Generation**. Observe que inicial- mente são importadas as três classes que criamos: Retriever, Augmentation e Generation. Em seguida, instanciamos cada uma delas. No caso do Retriever, utilizamos a coleção chamada "synthetic\_dataset\_papers", que foi construída anteriormente

quando indexamos 12 artigos em inglês sobre Banco de Dados Sin- téticos. Essa informação é fundamental, pois agora o sistema poderá recuperar trechos desses artigos para fundamentar a resposta.

Na sequência, definimos a variável query com a pergunta "What’s a synthetic dataset?". Essa consulta será utilizada para buscar trechos relevantes dentro da coleção indexada. O método search da classe Retriever retorna os chunks mais próximos semantica- mente da query, e esses trechos são então passados para o método generate\_prompt da classe Augmentation, que monta um prompt enriquecido combinando a pergunta e os pedaços de conhecimento selecionados. Esse prompt é entregue à classe Generation, que, utilizando o modelo gemini-2.5-flash, produz a resposta final em linguagem natural. Por fim, o resultado é impresso na tela, mostrando a saída gerada pelo RAG a partir dos artigos indexados.

**from retriever import Retriever**

**from augmentation import Augmentation from generation import Generation**

**retriever \= Retriever(collection\_name=" synthetic\_dataset\_papers")**

**augmentation \= Augmentation()**

**generation \= Generation(model="gemini-2.5-flash") query \= "What’s a synthetic dataset?"**

**\# Buscar documentos**

**chunks \= retriever.search(query, n\_results=10, show\_metadata=False)**  
**prompt \= augmentation.generate\_prompt(query, chunks)**

**\# Gerar resposta**

**response \= generation.generate(prompt) print(response)**

agora vou adicionar "Streamlit"ao código e executar o arquivo

**app.py** que está no projeto usando:

**streamlit run app.py**

A figura abaixo é o resultado da execução do RAG com Streamlit.

**2.13 EXERCÍCIOS**

Para consolidar os conceitos apresentados neste capítulo sobre o RAG Clássico, resolva os exercícios abaixo. Eles foram elaborados para estimular tanto a compreensão teórica quanto a prática de implementação em Python.

1. Explique com suas próprias palavras qual foi a principal limitação dos LLMs que levou ao surgimento do RAG Clássico.  
2. Diferencie **corpus** e **embedding**. Dê um exemplo prático para cada um deles.  
3. Descreva em que consiste a fase de **Indexing** e explique por que ela é considerada offline.  
4. Qual a função do parâmetro **chunk\_overlap** na classe Chunks? Dê um exemplo de como ele evita a perda de contexto.  
5. Utilize a classe ReadFiles para converter ao menos dois ar- quivos PDF para markdown. Mostre o resultado em um único arquivo concatenado.  
6. Gere embeddings para três frases de sua escolha utilizando o modelo

   paraphrase-multilingual-MiniLM-L12-v2 e verifique o ta- manho do vetor retornado.

7. Crie uma coleção no ChromaDB chamada meu\_corpus\_teste e insira ao menos cinco chunks. Em seguida, utilize o método count() para verificar quantos documentos foram armazena- dos.  
8. Explique a diferença entre o papel do **Retriever** e do **Augmented**. Por que não podemos pular a etapa de aumento de informação?  
9. Implemente uma pequena aplicação em Python que recebe uma **query** do usuário, recupera três chunks relevantes no ChromaDB e monta o prompt final com a classe Augmentation.  
10. Explique o conceito de **Adapter** no contexto da classe Generation. Por que ele é importante para desacoplar o código do provedor  
11. 

de LLM utilizado?

**CAPÍTULO	3**  
Rag com Memória

Imagine um professor que não apenas responde perguntas de seus alunos usando livros e artigos, mas que também se lembra de todas as conversas passadas em sala de aula. Esse professor não precisaria repetir explicações já dadas e conseguiria contextualizar cada nova pergunta com base no que já foi discutido. De forma análoga, o RAG com memória amplia as capacidades de um modelo de linguagem ao unir a recuperação de informações externas com a lembrança contínua de interações anteriores.

O RAG tradicional funciona como um consultor que tem acesso imediato a uma vasta biblioteca. Ele consulta as fontes a cada pergunta, mas não necessariamente se recorda do diálogo que já ocorreu. Isso garante precisão factual, mas pode limitar a continu- idade da experiência, já que cada resposta é construída como se fosse a primeira. Ao incorporar memória, passamos a ter um con- sultor que anota, organiza e retoma pontos importantes ao longo da jornada.

Essa evolução traz um aspecto fundamental: o contexto não se esgota na consulta isolada, mas se prolonga em uma linha narra- tiva. O sistema consegue retomar tópicos discutidos em interações passadas, adaptar suas respostas conforme o histórico e até corrigir mal-entendidos com base em lembranças. Esse tipo de continuidade é particularmente útil em aplicações educacionais, jurídicas, médicas e em qualquer domínio onde a progressão do diálogo importa tanto quanto a resposta imediata.

É nesse cenário que entra o conceito de memória no RAG. Ao unir o mecanismo de **recuperação** com a capacidade de reter conversas passadas, criamos um sistema híbrido mais próximo da forma como os humanos constroem conhecimento. Cada nova pergunta deixa de ser um evento isolado e passa a ser parte de uma trajetória de aprendizado ou investigação. Essa memória pode ser temporária, descartada após certo período, ou persistente, armazenada para uso contínuo.

Por fim, é importante notar que essa integração não se trata apenas de armazenar dados, mas de criar uma dinâmica onde a **geração**, a **memória** e a **recuperação** trabalham em conjunto. A memória fornece continuidade, a recuperação garante precisão e a geração traz fluidez na linguagem. O resultado é um RAG que não apenas responde, mas acompanha, evolui e participa de um diálogo de longo prazo com o usuário.

Figura 3.1: RAG com Memória é acoplado ao aumento de informações "Augmentedl"

**Baixando o Projeto**

Para começar, faça o download do nosso projeto no link abaixo:

**Link do projeto:**

[https://bit.ly/sandeco-rag-memory](https://bit.ly/sandeco-rag-memory)

**3.1 CRIANDO A MEMÓRIA COM O REDIS**

Para que o RAG consiga se lembrar de interações passadas, precisamos de um mecanismo de armazenamento rápido, confiável e que permita o acesso a dados em tempo real. Nesse ponto, entra o Redis. Pense no Redis como um quadro branco colocado no centro de uma sala: todos podem escrever nele, apagar ou atualizar anotações, e o acesso é imediato. Ele não é apenas um banco de dados tradicional, mas um sistema de armazenamento em memória, desenhado para velocidade extrema e simplicidade.

O Redis é um banco de dados do tipo chave-valor, o que signi- fica que cada informação é armazenada como um par: uma chave única que identifica os dados e o valor correspondente que contém o conteúdo. Essa estrutura simples é poderosa porque permite recu- perar informações em questão de milissegundos. No caso do RAG, cada conversa pode ser registrada sob uma chave que representa o identificador do usuário ou da conversa, enquanto o histórico de mensagens é o valor associado.

Uma das grandes vantagens do Redis é sua capacidade de traba- lhar totalmente em memória, o que reduz drasticamente a latência. Em outras palavras, ao invés de buscar os dados em disco rígido como bancos relacionais tradicionais, o Redis mantém tudo direta- mente na memória RAM. Isso faz com que operações de escrita e leitura sejam quase instantâneas, característica essencial para aplica- ções interativas como assistentes baseados em RAG que dependem

de fluidez no diálogo.

Além disso, o Redis possui recursos adicionais que o tornam ainda mais adequado para o papel de memória. Ele permite configurar expiração automática de dados, garantindo que informações antigas possam ser descartadas após um tempo definido, por exemplo: 24h, 5 dias ou 1 semana. Isso é particularmente útil em cenários nos quais não faz sentido manter diálogos antigos para sempre. Dessa forma, conseguimos um equilíbrio entre desempenho, praticidade e controle do ciclo de vida das conversas armazenadas.

**3.2 REDIS NO DOCKER**

Não existe Redis para Windows e o Docker é uma ferramenta indispensável quando falamos de facilidade e padronização na ins- talação de aplicações como a Redis. Ele permite que você crie um ambiente isolado para rodar o banco, sem se preocupar com as configurações específicas do sistema operacional ou conflitos entre dependências. Com o Docker, tudo o que você precisa está encapsulado em um contêiner, garantindo que o ambiente de exe- cução seja idêntico ao utilizado em produção. Essa abordagem elimina a famosa frase ’na minha máquina funciona’, proporcionando

consistência desde o desenvolvimento até o deploy.

Para os usuários do Windows, utilizaremos o Docker Desktop, uma interface amigável que facilita o gerenciamento dos contêineres e imagens necessários para rodar a Redis localmente. Esse processo não apenas agiliza a configuração do ambiente, mas também cria um espaço seguro para você desenvolver e testar a aplicação antes de implantá-la em uma VPS ou outro servidor remoto. O Docker Desktop transforma sua máquina local em uma plataforma robusta para experimentação, garantindo que você esteja pronto para levar seu projeto ao próximo nível com confiança.

**Instalando o Docker Desktop para Windows**

Vamos nessa, vamos instalar o Docker Desktop, que é a maneira mais fácil de gerenciar contêineres no Windows. Siga os passos abaixo para realizar a instalação de forma rápida e sem complica- ções:

**Passo 1: Baixar o Docker Desktop**

Acesse o site oficial do Docker através do link [https://www.](https://www.docker.com/products/docker-desktop) [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) e baixe a versão do Doc- ker Desktop compatível com o seu sistema operacional. Certifique-se de que está utilizando o Windows 10 ou superior, com suporte para o WSL2 (Windows Subsystem for Linux), que é um requisito para rodar o Docker Desktop.

**Passo 2: Instalar o Docker Desktop**

Após o download, execute o instalador e siga as instruções na tela. Finalize o processo e reinicie o computador.

**Passo 3: Iniciar o Docker Desktop**

Com tudo configurado, abra o Docker Desktop. Na primeira exe- cução, ele pode solicitar permissões administrativas para configurar o ambiente. Após a inicialização, verifique se o Docker está rodando corretamente observando o ícone na barra de tarefas.

CAPÍTULO 3\.

 	RAG COM MEMÓRIA

 	*67*

**Passo 5: Testar a Instalação**

Para garantir que o Docker está funcionando, abra o terminal ou o PowerShell e execute:

docker \--version

Se o comando retornar a versão do Docker 28.1.1 ou superior instalada, tudo está pronto para usarmos o Docker no nosso projeto Redis\!

**3.3 INSTALANDO O REDIS**

Para rodarmos o Redis de forma simples e organizada, utilizare- mos o Docker Compose. O arquivo docker-compose.yml centraliza todas as configurações necessárias e permite que o serviço seja inicializado com apenas um comando.

Abra o arquivo docker-compose.yml na raiz do projeto com o conteúdo abaixo:

**services: redis:**

**image: redis:7-alpine container\_name: redis-rag ports:**

**\- "6379:6379"**

**volumes:**  
**\- redis\_data:/data**

**command: redis-server \--appendonly yes restart: unless-stopped**

**healthcheck:**

**test: \["CMD", "redis-cli", "ping"\] interval: 10s**

**timeout: 3s retries: 3**

**volumes: redis\_data:**

**driver: local**

Nesse arquivo, alguns pontos merecem destaque:

* Utilizamos a imagem **redis:7-alpine**, que é leve e otimizada para produção.  
  * O contêiner será criado com o nome **redis-rag**.  
  * A porta **6379** é exposta localmente, permitindo a comunicação com a aplicação.  
  * O volume **redis\_data** garante persistência dos dados.  
  * O comando **redis-server –appendonly yes** ativa o modo de per- sistência em disco (AOF), evitando perda de dados em reinícios.  
  * A política de reinício **unless-stopped** assegura que o contêiner volte a rodar caso o sistema reinicie.  
  * O **healthcheck** executa periodicamente o comando **redis-cli ping** para verificar se o Redis está saudável.  
    Com o arquivo pronto, basta iniciar o Redis rodando no terminal (CMD) do Windows:

**docker-compose up \-d**

Depois, confirme se o Redis está ativo com:

**docker exec \-it redis-rag redis-cli ping**

Se tudo estiver correto, a resposta será ’PONG’, indicando que o Redis está em pleno funcionamento e pronto para ser usado como memória no RAG.

**3.4 CRIANDO A MÉMÓRIA**

Para simplificar o processo de adoção da memória, criamos uma classe chamada *Memory* no arquivo ’memory.py’. Essa classe foi organizada em partes que facilitam tanto a inicialização quanto o gerenciamento do histórico de conversas no Redis. Vamos entender cada uma delas.

Primeiro, observe os imports que são utilizados. Execute o carre- gamento das bibliotecas necessárias: o pacote *redis* para conexão com o banco, o *json* para serialização dos dados, o *time* para con- trole de tempo em alguns trechos, e os tipos do *typing* para melhor documentação do código.

**import redis import json import time**

**from typing import List, Dict, Any, Optional**

Em seguida, definimos a classe *Memory*. Nela declaramos uma constante que representa o tempo padrão de expiração das conver- sas em segundos, equivalente a 24 horas. Esse tempo será utilizado caso não seja passado nenhum valor diferente na inicialização da classe.

**class Memory:**

**"""**

**Uma classe para gerenciar o histórico de conversas de chat no Redis.**

**"""**

**DEFAULT\_EXPIRATION\_SECONDS \= 24 \* 60 \* 60 \# 24**  
**horas**

Agora, implemente o método construtor. Aqui, criamos uma co-

nexão com o Redis especificando o host, a porta e o banco a ser usado. Verifique se a conexão foi estabelecida utilizando o comando *ping*. Caso esteja tudo correto, exiba uma mensagem de confirma- ção. Caso contrário, dispare uma exceção interrompendo a execução. Note que também definimos a variável *expiration*, que vai armazenar o tempo de vida configurado para as chaves.

**def**	**init**	**(self, expiration\_seconds: int \= DEFAULT\_EXPIRATION\_SECONDS):**  
**redis\_client \= redis.Redis(host=’localhost ’, port=6379, db=0, decode\_responses=True)**  
**ping\_result \= redis\_client.ping() if ping\_result:**

**print("Conectado ao Redis\!\\n") else:**

**print("Falha na conexão com o Redis.") raise Exception("Falha na conexão com**

**o Redis.")**

**self.redis \= redis\_client self.expiration \= expiration\_seconds print(f"ChatManager inicializado. As**

**conversas expirarão em {self.expiration} segundos.")**

Na sequência, implemente um método auxiliar chamado \_get\_key. Ele serve para padronizar o formato das chaves que serão utilizadas no Redis. Escreva esse método de modo que, ao receber um *talk\_id*, ele devolva uma chave de string com prefixo ’conversation:’ seguido do identificador da conversa.

**def \_get\_key(self, talk\_id: str) \-\> str: """Método auxiliar para gerar a chave**

**padronizada do Redis."""**  
**return f"conversation:{talk\_id}"**

Em seguida, utilize o método *add\_memory*. Esse é o coração da classe, pois adiciona ou atualiza mensagens de uma conversa. Pri- meiro, obtenha a chave padronizada. Depois, busque no Redis se já existe algum histórico. Caso exista, carregue o conteúdo em formato JSON. Se não existir, inicialize com uma lista vazia e informe que uma nova conversa foi criada. Após isso, insira a nova mensagem no início da lista, serialize novamente em JSON e salve de volta no Redis, aplicando a expiração configurada.

**def add\_memory(self, talk\_id: str, role: str, message: str) \-\> None:**  
**key \= self.\_get\_key(talk\_id)**  
**existing\_history\_json \= self.redis.get(key**

**)**

**if existing\_history\_json: history \= json.loads(**  
**existing\_history\_json)**

**else:**

**history \= \[\]**

**print(f"Nova conversa sendo criada para o usuário ’{talk\_id}’.")**

**history.insert(0, {"role": role, "content"**

**: message})**

**updated\_history\_json \= json.dumps(history) self.redis.set(key, updated\_history\_json,**

**ex=self.expiration)**

**print(f"Memória de ’{talk\_id}’ atualizada com a mensagem de ’{role}’.")**

Crie também o método *get\_conversation*. Ele deve recuperar uma conversa completa a partir do *talk\_id*. Para isso, obtenha a chave, faça a leitura no Redis e, caso o conteúdo exista, carregue o JSON

para devolver uma lista de mensagens. Caso contrário, retorne *None*.

**def get\_conversation(self, talk\_id: str) \-\> Optional\[List\[Dict\[str, Any\]\]\]:**  
**key \= self.\_get\_key(talk\_id)**  
**history\_json \= self.redis.get(key)**

**if history\_json:**  
**return json.loads(history\_json)**

**return None**

Implemente também o método *delete\_conversation*. Ele deleta o histórico de uma conversa armazenada no Redis. Se a exclusão ocorrer, exiba uma mensagem confirmando. Se não houver conversa associada ao *talk\_id*, mostre apenas uma informação de que nada foi removido.

**def delete\_conversation(self, talk\_id: str) \-\> None:**  
**key \= self.\_get\_key(talk\_id)**

**if self.redis.delete(key) \> 0: print(f"Conversa para o usuário ’{**  
**talk\_id}’ foi deletada.")**

**else:**

**print(f" Nenhuma conversa para o usuá rio ’{talk\_id}’ foi encontrada para deletar.")**

Por fim, observe o bloco principal. Execute a criação de um objeto da classe *Memory*. Defina um *TALK\_ID* para identificar a conversa e, em seguida, delete qualquer histórico anterior com esse identificador. Adicione mensagens na sequência, simulando um diálogo entre usuário e sistema. Use *time.sleep* para criar pequenas pausas, e por último recupere e exiba a conversa final, incluindo o tempo de vida restante (*ttl*) no Redis.

**if**		**name**	**\== "** 	 **main**	**": try:**  
**chat\_manager \= Memory()**

**TALK\_ID \= "sandeco-upsert-test"**

**chat\_manager.delete\_conversation(TALK\_ID) print("-" \* 30\)**

**chat\_manager.add\_memory(TALK\_ID, "user", " Qual o primeiro livro de Isaac Asimov?")**

**time.sleep(1) chat\_manager.add\_memory(TALK\_ID, "system",**

**"O primeiro romance publicado por Isaac Asimov foi ’Pebble in the Sky’ (1950).")**

**time.sleep(1) chat\_manager.add\_memory(TALK\_ID, "user", "**

**Obrigado\!")**

**conversa\_final \= chat\_manager. get\_conversation(TALK\_ID)**  
**if conversa\_final:**  
**key \= chat\_manager.\_get\_key(TALK\_ID) ttl \= chat\_manager.redis.ttl(key) print(f"\\n--- Conversa Final**

**Recuperada (expira em {ttl}s) \---") for msg in conversa\_final:**

**print(f"	\[{msg\[’role’\].upper()}\]:**

**{msg\[’content’\]}")**

**print("-" \* 50\)**

**except redis.exceptions.ConnectionError as e: print(f"Falha na conexão com o Redis: {e}"**

**)**

**3.5 ADICIONANDO A MEMÓRIA AO RAG**

Para que o RAG passe a trabalhar com memória, precisamos alterar o ponto onde ocorre a junção das informações. Essencial- mente, a mudança está concentrada na classe *Augmentation*, ou seja, no **A do RAG**. Essa classe é responsável por reunir os dados recuperados (**Retriever**) e organizar o contexto que será enviado para a *Generation*, o **G do RAG**.

O que fazemos agora é acrescentar ao *Augmentation* a capaci- dade de lidar com memória. Isso significa que, além de juntar os *chunks* recuperados, o prompt também será complementado com o histórico das conversas anteriores. Dessa forma, o modelo não responde de maneira isolada a cada consulta, mas leva em conta a sequência do diálogo. Observe que o parâmetro *talk\_id* identifica a conversa, permitindo que diferentes usuários tenham seus históricos separados.

Outro ponto importante é que, no código principal, precisamos enviar para a memória tudo aquilo que a *Generation* produzir. Isso garante que, ao gerar uma nova resposta, ela será armazenada e poderá ser recuperada em interações futuras. A memória então passa a registrar tanto a pergunta formatada pelo *Augmentation* quanto a resposta produzida pela *Generation*.

Veja a seguir como a classe *Augmentation* foi modificada. Com- pare com a versão anterior, onde apenas o prompt era construído. Agora, além de gerar o prompt, adicionamos métodos para limpar a memória, registrar novas interações e recuperar o histórico:

**from memory\_rag import MemoryRAG**

**class Augmentation:**  
**def**	**init**	**(self, talk\_id):**

**self.talk\_id \= talk\_id self.memory\_rag \= MemoryRAG() self.prompt \= ""**

**def generate\_prompt(self, query\_text, chunks): separador \= "\\n\\n------------------------\\**

**n\\n"**

   
**chunks\_formatados \= f"Conhecimento\\n**

**\------------------------\\n\\n{separador.join( chunks)}"**

**self.prompt \= f"""Responda em pt-br e em markdown, a query do usuário delimitada por \< query\>**

**usando apenas o conhecimento dos chunks delimitados por \<chunks\>**

**e tenha em mente o historico das conversas anteriores delimitado por \<historico\>.**

**Combine as informações para responder a query de forma unificada. A prioridade**

**das informações são: query=1, chunks=2, historico=3.**

**Se por acaso o conhecimento não for suficiente para responder a query,**

**responda apenas que não temos conhecimento suficiente para responder**

**a Pergunta.**

**\<chunks\>**  
**{chunks\_formatados}**

**\</chunks\>**

**\<query\>**  
**{query\_text}**

**\</query\>**

**\<historico\>**

**{self.memory\_rag.get\_conversation(self. talk\_id)}**

**\</historico\> """**

**return self.prompt**

**def clear\_memory(self): self.memory\_rag.delete\_conversation(self.**  
**talk\_id)**

**def add\_memory(self, llm\_response): try:**  
**self.memory\_rag.add\_memory(self.**  
**talk\_id, "user", self.prompt)**

**self.memory\_rag.add\_memory(self. talk\_id, "system", llm\_response)**

**return True  except Exception as e:**

**print(f"Erro ao adicionar memória: {**

**str(e)}")**

**return False**

**def get\_conversation(self):**

**return self.memory\_rag.get\_conversation( self.talk\_id)**

**Adaptando o código principal**

Agora que já estruturamos as classes individuais do RAG com memória, podemos observar o código principal que conecta todas

elas em um fluxo contínuo. Esse trecho é responsável por coordenar a **recuperação**, a **montagem do prompt com memória** e a **geração da resposta**. Vamos entender como cada parte funciona.

Primeiro, faça as importações das três classes centrais: *Retriever*, *Augmentation* e *Generation*. São elas que representam, respectiva- mente, o R, o A e o G do RAG.

**\# arquivo main.py do projeto from retriever import Retriever**

**from augmentation import Augmentation from generation import Generation**

Em seguida, defina um identificador de conversa chamado *TALK\_ID*. Esse valor será usado pela memória para associar as perguntas e respostas a uma mesma sessão.	Depois disso, inicialize as ins- tâncias de cada classe: o *Retriever* apontando para a coleção de dados a ser consultada, o *Augmentation* recebendo o *TALK\_ID*, e o *Generation* configurado com o modelo de linguagem escolhido.

**TALK\_ID \= "sandeco-chat-001"**

**retriever \= Retriever(collection\_name=" synthetic\_dataset\_papers")**  
**augmentation \= Augmentation(talk\_id=TALK\_ID) generation \= Generation(model="gemini-2.5-flash")**

Agora, construa o laço principal da aplicação. Dentro do *while True*, capture a entrada do usuário simulando um chat. Se a pessoa digitar a palavra ’sair’, o sistema interrompe a execução e encerra o loop.

**while True:**  
**user\_query \= input("Sua Pergunta: ")**

**if user\_query.lower() \== ’sair’:**

**print("Até a próxima\!") break**

Caso a entrada não seja ’sair’, execute o fluxo do RAG. Primeiro, use o *Retriever* para buscar os *chunks* relevantes. Em seguida, utilize o *Augmentation* para gerar o prompt que combina a query, os chunks recuperados e o histórico da memória. Depois, chame o *Generation* para produzir a resposta final a partir desse prompt. Note que logo após gerar a resposta, o sistema a envia de volta para a memória utilizando *augmentation.add\_memory(response)*. Por fim, exiba a resposta na tela.

**chunks \= retriever.search(user\_query, n\_results=10, show\_metadata=False)**  
**prompt \= augmentation.generate\_prompt( user\_query, chunks)**

**response \= generation.generate(prompt) augmentation.add\_memory(response)**

**print(response)**

Esse fluxo garante que a cada interação o modelo consulte infor- mações externas, construa um contexto atualizado com o histórico da conversa e registre a nova resposta na memória. Assim, o RAG deixa de ser uma sequência de chamadas independentes e passa a manter coerência ao longo de todo o diálogo.

Com isso, criamos um fluxo contínuo: o **Retriever** busca a infor- mação, o **Augmentation** constrói o prompt incluindo o histórico, o **Generation** gera a resposta, e finalmente essa resposta é enviada de volta para a memória. Dessa forma, o RAG não apenas responde, mas passa a acompanhar e registrar toda a interação. Agora é só executar a main.py e conversar com o RAG.

**3.6 EXERCÍCIOS**

1. Explique, com suas próprias palavras, qual a diferença entre um RAG tradicional e um RAG com memória. Use a analogia do professor apresentada na abertura do capítulo como apoio.  
2. Analise o papel da classe *Memory*. O que acontece se o método *add\_memory* não for chamado após cada resposta gerada pelo modelo?  
3. No fluxo principal, identifique em que ponto a resposta do modelo é enviada de volta para a memória. Por que esse passo é fundamental para manter a coerência do diálogo?  
4. Modifique o código da classe *Augmentation* para que apenas as últimas três interações sejam incluídas no histórico ao gerar o prompt. Qual seria o impacto dessa modificação no comporta- mento do RAG?  
5. Crie um teste em que duas sessões de conversa (*TALK\_ID* diferentes) sejam executadas simultaneamente. Mostre como o sistema mantém o histórico separado para cada sessão.  
6. Reflita sobre cenários em que a expiração das conversas seja vantajosa. Em quais aplicações faz sentido que as memórias se apaguem após um tempo definido? E em quais não?  
7. No código principal, troque a condição de parada de ’sair’ para outro comando de sua escolha. Execute o programa e verifique se a lógica continua funcionando corretamente.  
8. Observe a ordem em que as mensagens são armazenadas na memória. Justifique por que a decisão de inserir a mensagem no início da lista é importante para a recuperação do histórico.  
9. Implemente uma função que mostre, a qualquer momento, o histórico completo da conversa atual. Utilize os métodos já existentes na classe *Memory*.  
10. Imagine que você está aplicando esse RAG com memória em um ambiente educacional. Proponha um exemplo de como essa  
11. 

funcionalidade poderia melhorar a experiência do estudante em comparação a um RAG sem memória.

**CAPÍTULO	4**  
RAG Autônomo com Agentic RAG

Imagine que agora você tem várias bases de dados vetoriais espalhadas, cada uma especializada em um domínio específico: direito, saúde, engenharia, literatura ou mesmo datasets sintéticos para experimentos. O desafio é que o usuário faz uma consulta e o RAG precisa saber para onde direcionar essa pergunta, escolhendo o fluxo mais adequado para encontrar a resposta correta. É aqui que entra o AgenticRAG.

Figura 4.1: AgenticRAG \- Direcionador de Fluxos

Pense no AgenticRAG como um guarda de trânsito cognitivo. Ele não dirige os carros, mas observa o fluxo e decide quem deve seguir,

quem deve parar e qual caminho cada veículo deve tomar para chegar ao destino certo. Da mesma forma, o AgenticRAG direciona a consulta do usuário para a base de dados mais apropriada, organiza o fluxo de recuperação e garante que a resposta volte de forma coerente e contextualizada.

Enquanto um RAG tradicional consulta uma fonte única ou de- pende de configuração estática, o AgenticRAG atua com autonomia: ele avalia a pergunta, decide qual vetorstore ou qual ferramenta acio- nar e orquestra as etapas de raciocínio. Em vez de depender apenas de regras pré-programadas, o agente opera de forma adaptativa, mudando a estratégia conforme a natureza da consulta.

Ao longo deste capítulo, vamos detalhar como projetar essa arqui- tetura, explorando a lógica de roteamento, os blocos que conferem autonomia ao agente e exemplos práticos de como o AgenticRAG pode se tornar o ’guarda de trânsito’ do conhecimento. Dessa forma, o RAG deixa de ser apenas um mecanismo de busca e passa a agir como um orquestrador inteligente, capaz de conduzir cada consulta para o fluxo mais eficiente.

**Baixando o Projeto**

Para começar, faça o download do nosso projeto no link abaixo:

**Link do projeto:**

[https://bit.ly/sandeco-agentic-rag](https://bit.ly/sandeco-agentic-rag)

**4.1 AGENTICRAG**

Com o crescimento do uso de Agentes de IA, surge a necessi- dade de integrar essa autonomia ao próprio RAG, criando o que chamamos de **AgenticRAG**. Nesse modelo, o agente não é apenas um componente auxiliar, mas a peça central que direciona o fluxo de

informações de acordo com a consulta feita pelo usuário. Ele atua como um orquestrador, capaz de decidir de forma inteligente para qual base de dados vetorial encaminhar a pergunta, quando acionar embeddings adicionais e como estruturar o processo de recuperação antes de entregar o resultado para a geração. Essa camada de decisão transforma o RAG em um sistema mais flexível e adaptativo, pronto para lidar com cenários complexos onde múltiplas fontes e estratégias podem estar envolvidas.

Ao adotar essa abordagem, o RAG deixa de ser apenas uma sequência linear de etapas e passa a se comportar como um sistema dinâmico, no qual o agente avalia continuamente a melhor rota para cada consulta. Pense no AgenticRAG como um guarda de trânsito: ele não dirige os carros, mas observa o tráfego, interpreta a situa- ção e indica o caminho correto. Assim, em vez de enviar todas as queries para a mesma direção, o agente distribui as consultas para o fluxo mais apropriado, garantindo que a resposta seja construída de maneira mais eficiente e contextualizada.

Na Figura do fluxo RAG, você pode observar claramente essa mudança. O usuário envia a query, mas ela não segue diretamente para o **Retriever**. O primeiro ponto de contato é o **Agente**, destacado em verde, que assume o papel de orquestrador. Veja como o fluxo é conduzido: o agente recebe a consulta, pode acionar o módulo de **Embedding** para enriquecer a representação semântica e, em seguida, decide qual dataset será utilizado.

CAPÍTULO 4\.

RAG AUTÔNOMO COM AGENTIC RAG	85

Note que o **Augmented** continua a organizar o contexto antes de passá-lo para a **Generation**, mas agora todo esse processo é enriquecido pela decisão inicial do agente. A lógica do fluxo se torna: usuário envia a query → agente interpreta e direciona → embeddings e datasets são acionados → recuperação é feita → augmentation organiza → geração devolve a resposta. Essa mudança estrutural é o que diferencia o AgenticRAG, tornando-o mais robusto e inteligente no direcionamento das consultas.

**4.2 CLASSE DE REGISTRO DE DATASETS**

A primeira coisa que precisamos fazer é criar um registrador de datasets. Para criar um novo dataset (collection no ChromaDB), você deve usar a classe do código ’semantic\_encoder.py’, explicada na Seção [2.8](#bookmark=id.io61ni3m3ncp) do Capítulo [2\.](#bookmark=id.wen5w9klbt0q)

Após a criação, registre o novo dataset na classe **Datasets**, que terá a responsabilidade de armazenar todas as coleções de dados disponíveis para o Agentic RAG. Essa classe será usada para infor- mar ao nosso agente de roteamento de fluxo quais datasets e quais assuntos estão disponíveis.

Observe que, no construtor da classe **Datasets**, representado pelo método init  , é inicializada uma lista chamada **datasets**. Nela, escreva cada base de conhecimento como um dicionário, de- finindo três atributos fundamentais: o nome interno do dataset, a descrição que explica em que contexto ele deve ser pelo agente e o **locale**, que indica a língua predominante do material.

O primeiro registro é o dataset chamado **synthetic\_dataset\_papers**, que possui uma descrição clara de que deve ser usado quando a consulta envolver a construção, utilização ou detecção com dados sin- téticos. Seu locale é definido como ’en’, reforçando que esse conjunto está em inglês.  Em seguida, temos o segundo registro: o dataset chamado **direito\_constitucional**, que será escolhido sempre que a consulta envolver temas jurídicos, leis, processos ou jurisprudência.

Nesse caso, o locale é ’pt-br’, garantindo que a base de dados esteja

em português e seja adequada ao contexto legal brasileiro.

Informar o **locale** do dataset pode ajudar a traduzir a query para a língua predominante nos chunks, gerando uma consulta mais efetiva e possibilitando ao usuário flexibilidade para escrever a query em sua língua nativa.

**class Datasets:**

**def**	**init**	**(self): self.datasets \= \[**  
**{"dataset": "synthetic\_dataset\_papers"**

**,**

**"description": "A construção, utilizaç ão ou detecção usando**

**datasets sintéticos", "locale": "en"},**

**{"dataset": "direito\_constitucional", "description": "Se a consulta envolver**

**direito, leis,**

**processos ou jurisprudência", "locale": "pt-br"}**

**\]**

Agora vamos começar a criar nossos agentes. Existem duas for- mas principais de fazer isso. A primeira consiste em enviar a consulta diretamente para a LLM de sua escolha, utilizando a API correspon- dente. A segunda forma é criar o agente por meio de um framework, como CrewAI, ADK ou outros semelhantes. Independentemente da forma escolhida, todos os agentes que você desenvolver devem estender a classe **AgentRAGAbstract**, o que facilitará a construção e a organização do fluxo do RAG.

**4.3 AGENTE ABSTRATO**

Aqui vamos abordar um conceito diferenciado na criação de agen- tes: a definição de um agente abstrato que servirá como template para os demais. Essencialmente, esse agente abstrato é implemen- tado como uma classe abstrata.

Pense em uma classe abstrata como a planta de um prédio que ainda não foi construído. A planta define quantos andares existirão, onde estarão os elevadores, as escadas e a estrutura básica que todos os andares devem seguir. Porém, cada andar só ganha vida quando os engenheiros e arquitetos decidem como será decorado, quais materiais serão usados e quais salas existirão. Assim também funciona a classe abstrata: ela define a estrutura mínima que todas as subclasses precisam respeitar, mas deixa a cargo de cada uma a implementação específica dos detalhes.

Uma classe abstrata é um recurso essencial da programação orientada a objetos quando se deseja criar um molde para outras classes. Execute a criação de uma classe abstrata sempre que precisar definir uma estrutura mínima obrigatória que outras classes deverão seguir. Ela não pode ser instanciada diretamente, mas serve como um contrato que obriga suas subclasses a implementar determinados métodos. Isso garante que todas as classes derivadas mantenham um padrão de comportamento, mesmo que internamente a implementação varie.

Além disso,  utilize classes abstratas quando quiser organizar hierarquias de objetos que compartilham características comuns, mas que ainda exigem especialização em pontos específicos.  Ao declarar métodos abstratos, você determina que qualquer classe filha seja obrigada a escrever sua própria versão desses métodos. Isso evita inconsistências e assegura que o fluxo definido como regra seja respeitado em toda a aplicação, mantendo uniformidade no projeto.

No código da classe **AgentRAGAbstract**, observe que ela herda de **ABC**, que é a classe base para construção de classes abstratas no Python. Dentro do construtor, execute a inicialização da variável **datasets**, que recebe a instância da classe **Datasets**. Essa escolha garante que qualquer agente que estenda **AgentRAGAbstract** já terá acesso imediato ao registrador de datasets, sem precisar reim- plementar essa lógica a cada nova classe. Com isso, você centraliza e padroniza o acesso às bases de dados disponíveis no RAG.

Por fim, repare no método **query**, declarado com o decorador

**@abstractmethod**. Esse detalhe indica que não existe implementa-

**class AgentRAGAbstract(ABC):**  
**def**	**init**	**(self):**

**self.datasets \= Datasets()**  
**@abstractmethod**

**def query(self, query): pass**

ção padrão para esse método, e que todas as subclasses da **AgentRAGAbstract** deverão obrigatoriamente escrevê-lo. Faça a im- plementação de cada agente, definindo como ele receberá a consulta, processará a query e interagirá com os datasets.  Essa estratégia garante que todos os agentes mantenham uma interface comum, facilitando a integração no fluxo do RAG e a consistência entre di- ferentes tipos de agentes. Você verá que todos os nossos agentes terão esse método **query**.

|  \#agentRAGAbstract.py |  dentro da past |  agentRAG |
| :---- | :---- | :---- |
| **from abc import ABC, from datasets import** | **abstractmethod Datasets** |  |

**4.4 AGENTE COM API DA LLM**

Como já mencionei anteriormente, é possível criar agentes uti- lizando frameworks ou chamando diretamente a API de uma LLM. No entanto, adoto uma regra prática: se o projeto exige apenas um único agente que somente acessa uma LLM, não faz sentido carregar todo um framework de agentes na memória apenas para realizar

uma chamada simples à LLM. Nesses casos, prefira a chamada direta, pois ela torna o fluxo mais leve, eficiente e sem sobrecarga desnecessária. Por isso, vamos criar aqui nesta seção um código de agente simples sem framework e na próxima seção usaremos um framework para exemplificar, ok?

**Gemini Agent**

Vamos criar a classe **AgentRAGemini** no arquivo agenticRAGe- mini.py. Veja que a classe estende **AgentRAGAbstract**, portanto, obrigatoriamente ela deve implementar o método **query**. A função desse agente é interagir com a API do Gemini, utilizando o modelo especificado, para escolher dinamicamente qual dataset será usado conforme a consulta recebida do usuário.

**\#instale o Google Genai uv add google-genai**

A primeira parte do código trata das importações. Execute a importação dos módulos essenciais como **os**, que será usado para acessar variáveis de ambiente, o pacote **genai** do Google, responsá- vel pela interação com o modelo Gemini, e o módulo **json**, necessário para manipular a resposta que virá no formato JSON. Também faça a importação da classe **AgentRAGAbstract**, que será estendida aqui para manter a padronização da arquitetura.

**import os**

**from google import genai import json**

**from .agentRAGAbstract import AgentRAGAbstract**

Em seguida, observe a definição da classe **AgentRAGemini**. No construtor, utilize o **super()** para herdar as inicializações da classe abstrata. Logo depois, configure a chave da API do Gemini com a

variável de ambiente **GEMINI\_API\_KEY** e defina o modelo a ser utili- zado, neste caso **gemini-2.5-flash**. Execute essa configuração inicial para que qualquer instância criada do agente já esteja preparada para se comunicar com a API do Gemini.

**class AgentRAGemini(AgentRAGAbstract):**

**def**	**init**	**(self): super().**	**init**	**()**

**\# Configurar API key do Gemini self.model \= "gemini-2.5-flash" self.client \= genai.Client(api\_key=os.**  
**getenv(’GEMINI\_API\_KEY’))**

A terceira parte do código é o método **create\_prompt**, respon- sável por construir dinamicamente o prompt que será enviado ao modelo. Escreva aqui a lógica que percorre todos os datasets regis- trados e formata suas descrições, nomes e locales dentro do texto. Note que o prompt exige que a saída seja estritamente em formato JSON, contendo os atributos **dataset\_name**, **locale** e **query**. O detalhe importante é que a query deve ser traduzida para o idioma definido pelo locale escolhido, garantindo consistência na comuni- cação com a base. Repare também nas instruções imperativas dentro do prompt, que restringem a saída apenas ao JSON, sem justificativas ou textos adicionais.

**def create\_prompt(self, query):**

**\# Construir descrição dos datasets prompt \= f’’’**

**Sua missão:**

**Com base na solicitação do usuário "{ query}" escolha**

**somente um dataset é mais apropriado da lista abaixo:**

**’’’**

**for dataset in self.datasets.datasets: prompt \+= f"- {dataset\[’description’\]}**

**escreva \-\>**

**{dataset\[’dataset’\]}. Dataset**

**Locale: {dataset\[’locale’\]}"**  
**prompt \+= r"""\\n**

**Eu quero como saida um json com as seguintes informações do dataset escolhido:**

- **dataset\_name:**  
- **locale:**  
- **query:**

**A query deve ser traduzida para o locale**

**do dataset escolhido.**

**Não adicione explicações, justificativas ou qualquer outro texto.**  
**Não adicione caracteres**

**caracteres de escape.**

**Não adicione ‘‘‘json ou json de resposta,**

**se vc colocar isso você**  
**especiais ou**  
**‘‘‘ envolvendo o**

**será demitido.**  
**Exemplo de saida:**  
**{"dataset\_name": "dataset", "locale": "en"**

**, "query": "This is my question"}**  
**É IMPERATIVO:**

**Não escreva nada além do json de resposta. """**  
**return prompt**

Por fim, analise o método **query**, que é a implementação obri- gatória da classe abstrata. Execute a criação do prompt usando o método anterior, depois envie esse prompt ao modelo Gemini por

meio da função **generate\_content**. O retorno da API chega como texto, portanto use o **json.loads** para convertê-lo em um dicionário Python. Ao final, retorne esse dicionário, que conterá as informações do dataset escolhido e a query traduzida. Essa etapa completa o ciclo: da consulta do usuário até a seleção automática do dataset adequado.

**def query(self, query): """**

**Implementa o método abstrato query para conectar com o Gemini**

**"""**

**\# Criar prompt com contexto  prompt \= self.create\_prompt(query)**

**response \= self.client.models. generate\_content(**

**model=f"models/{self.model}", contents=\[prompt\]**

**)**

**response \= json.loads(response.text) return response**

Viu como é simples nosso Agente com conexão direta com o Gemini?

Ah\!	Uma coisa importante,  não esqueça de colocar a sua GE- MINI\_API\_KEY no arquivo **.env**.

**GEMINI\_API\_KEY="sua\_chave\_aqui"**

**4.5 AGENTIC RAG COM CREWAI**

Já exploramos em profundidade o uso do **CrewAI** nos meus dois livros *Agentes Inteligentes Vol. 1* e *Vol. 2*. Por isso, vamos direto ao ponto na criação de um Agente RAG utilizando esse framework.

Primeiro devemos instalar o CrewAI no nosso projeto:

**uv add crewai**

Vamos criar a classe **AgentRAGCrewAI** no arquivo agenticRAG- crewAI.py. Veja que a classe também estende **AgentRAGAbstract** e, portanto, obrigatoriamente deve implementar o método **query**. A diferença aqui é que esse agente não utiliza a API do Gemini, mas sim o framework CrewAI para organizar o fluxo de decisão sobre qual dataset será usado. Essa integração permite que o agente use o conceito de equipes (**Crew**), compostas por agentes e tarefas, para gerenciar de forma mais estruturada o processo de escolha do dataset adequado.

Na primeira parte do código, execute a importação dos módulos necessários. O pacote **dotenv** é carregado para acessar variáveis de ambiente. Em seguida, importamos as classes **Crew**, **Agent**, **Task** e **Process** da biblioteca CrewAI, que são fundamentais para construir o fluxo. Também fazemos a importação da classe **Datasets** e de **AgentRAGAbstract**, que será estendida. Por fim, a biblioteca **json** será utilizada para manipular a saída do modelo. Logo abaixo, a função **load\_dotenv()** é executada para carregar as variáveis de ambiente definidas em um arquivo .env.

**from dotenv import load\_dotenv**

**from crewai import Crew, Agent, Task, Process from datasets import Datasets**

**from .agentRAGAbstract import AgentRAGAbstract**

**import json**

**load\_dotenv()**

Na sequência, definimos a classe **AgentRAGCrewAI**. Dentro do construtor init , atribuímos ao atributo **llm** o modelo que será utilizado, no caso, **gpt-5-mini**.

**class AgentRAGCrewAI(AgentRAGAbstract):**

**def**	**init**	**(self): self.llm \= "gpt-5-mini"**

A parte seguinte é o método **create\_crew**, responsável por cons- truir a equipe (**Crew**) que fará a decisão sobre qual dataset utilizar. Primeiro, criamos um agente chamado **router**, com um papel e ob- jetivo claros: decidir, com base na solicitação do usuário, qual base vetorial deve ser usada. Ele recebe também uma **backstory**, que fornece contexto ao agente sobre sua função, e parâmetros como **reasoning** e **verbose**, que controlam o nível de raciocínio e deta- lhamento da execução. Em seguida, é construída a descrição da tarefa usando o método **create\_description**, que gera um enunciado detalhado para o agente. Essa descrição é usada para compor um objeto **Task**, que define o nome da tarefa, o agente responsável, a descrição e o formato esperado da saída, que deve ser um JSON. Por fim, toda essa estrutura é organizada em uma instância de **Crew**, onde a tarefa é registrada e o processo de execução é configurado como sequencial.

**def create\_crew(self, query):**

**router \= Agent(**

**role="Agente Roteador de RAG", goal=(**

**"Decidir, com base na solicitação**

**do usuário, "**

**"qual base vetorial de conhecimento deve ser usada "**

**"para responder da forma mais**

**adequada."**

**),**

**backstory=(**

**"Você é um especialista em recuperação de informação e agente RAG. "**

**"Sua função é interpretar a solicitação e determinar**

**de forma precisa qual "**

**"dataset de conhecimento deve ser**

**consultado. "**

**),**

**reasoning=True, verbose=True, llm=self.llm**

**)**

**description, frase\_dataset\_name \= self. create\_description(query)**

**task \= Task(**

**name="Decidir dataset RAG", agent=router, description=description, expected\_output="Um json com as**

**informações do dataset escolhido e com a query traduzida para o locale do dataset escolhido",**

**llm=self.llm**

**)**

**self.crew \= Crew( agents=\[router\], tasks=\[task\], process=Process.sequential**

**)**

Agora observe o método **create\_description**. Ele monta a descri- ção que será usada pela tarefa, seguindo a mesma lógica explicada anteriormente no AgentRAGemini. O texto apresenta ao agente sua missão, lista todos os datasets disponíveis com suas descrições, nomes e locales, e instrui claramente que a saída deve ser apenas um JSON com os campos **dataset\_name**, **locale** e **query**. O detalhe importante é que a query deve ser traduzida para o locale do dataset escolhido. As instruções também reforçam restrições rígidas, como não adicionar explicações extras ou caracteres especiais, garantindo que a saída seja limpa e padronizada.

**def create\_description(self, query):**

**\# Construir descrição dos datasets description \= f’’’**

**Sua missão:**

**Com base na solicitação do usuário "{ query}" escolha**

**somente um dataset é mais apropriado da lista abaixo:**

**’’’**

**for dataset in self.datasets.datasets: description \+= f"- {dataset\[’**

**description’\]} escreva \-\> {dataset\[’dataset’\]}. Dataset Locale: {dataset\[’locale’\]}"**

**description \+= r"""\\n**

**Eu quero como saida um json com as seguintes informações do dataset escolhido:**

- **dataset\_name:**  
- **locale:**  
- **query:**

  **A query deve ser traduzida para o locale do dataset escolhido.**

  **Não adicione explicações, justificativas ou qualquer outro texto.**

  **Não adicione caracteres especiais ou caracteres de escape.**

  **Não adicione ‘‘‘json ou ‘‘‘ envolvendo o json de resposta, se vc colocar isso vc será demitido.**

  **Exemplo de saida:**

  **{"dataset\_name": "dataset", "locale": "en"**

  **, "query": "This is my question"}**




**É IMPERATIVO:**

**Não escreva nada além do json de resposta. """**

**return description**

Por fim, temos os métodos **kickoff** e **query**. O método **kickoff** é responsável por iniciar a execução da Crew criada anteriormente, retornando o resultado produzido pelo agente. Já o método **query** chama **kickoff**, recebe a resposta e, em seguida, converte o con- teúdo bruto para o formato JSON usando a função **json.dumps**. Esse processamento final garante que a resposta esteja no formato correto, pronta para ser interpretada pelo restante do fluxo do RAG. Dessa forma, completamos a implementação de um agente base- ado no CrewAI, totalmente integrado ao padrão definido pela classe abstrata.

**def kickoff(self, query): self.create\_crew(query)**

**response \= self.crew.kickoff() return response**

**def query(self, query):**

**response \= self.kickoff(query)**

**\# converta o json em string para que possa ser convertido em um objeto json**

**response.raw \= json.dumps(response.raw)**

**return response.raw**

**4.6 EXECUTANDO O AGENTIC RAG**

Agora vamos criar uma "main"para executar o nosso Agentic RAG. Essa será a parte responsável por orquestrar todo o fluxo: receber a consulta do usuário, decidir qual dataset utilizar, recuperar os docu- mentos relevantes, montar o prompt e, por fim, gerar a resposta. É aqui que todos os componentes que já desenvolvemos anteriormente se conectam em um pipeline contínuo.

Na primeira parte do código, execute a importação das classes que serão utilizadas. Três delas são fundamentais para compor o fluxo tradicional do RAG: **Retriever**, **Augmentation** e **Generation**. Além disso, importamos o **AgentRAGemini**, que será o agente res- ponsável por decidir qual dataset utilizar com base na query recebida do usuário. Esse conjunto de importações garante que todos os módulos estejam disponíveis para a execução.

**from retriever import Retriever**

**from augmentation import Augmentation from generation import Generation**

**from agentRAG.agenticRAGemini import AgentRAGemini**

Em seguida, observe a definição da query do usuário. Aqui, a per- gunta "O que é direito constitucional fala do abandono afetivo?"será usada como exemplo. Execute a criação de uma instância de **Agen- tRAGemini** e chame o método **query**, que retorna um dicionário em formato JSON. Esse dicionário contém, entre outras informações, o campo **dataset\_name**, indicando qual base vetorial foi escolhida pelo agente para responder à consulta. Armazene essa informação na variável **dataset\_escolhido** para utilizá-la nos próximos passos.

**query \= "O que é direito constitucional fala do abandono afetivo?"**

**dataset \= AgentRAGemini().query(query)**

**dataset\_escolhido \= dataset\[’dataset\_name’\]**

Na terceira parte, inicialize os três módulos centrais do RAG. O **Retriever** será criado recebendo como parâmetro a coleção cor- respondente ao dataset escolhido. O **Augmentation** é instanciado em seguida, sendo responsável por montar o prompt final. Já o **Generation** é inicializado especificando o modelo a ser usado, neste caso **gemini-2.5-flash**. Essa etapa configura o fluxo para que cada componente saiba exatamente qual papel desempenhar.

**retriever \= Retriever(collection\_name= dataset\_escolhido)**

**augmentation \= Augmentation()**

**generation \= Generation(model="gemini-2.5-flash")**

Agora execute a recuperação e geração de resposta. Use o **Re- triever** para buscar documentos relevantes à query, pedindo dez resultados e omitindo metadados. Em seguida, passe esses resulta- dos ao método **generate\_prompt** do **Augmentation**, que cria um prompt estruturado combinando a query e os chunks recuperados. Esse prompt é então enviado ao módulo **Generation**, que gera a resposta final. Por último, exiba o resultado com o comando **print**, completando o ciclo do Agentic RAG em funcionamento.

**\# Buscar documentos**

**chunks \= retriever.search(query, n\_results=10, show\_metadata=False)**  
**prompt \= augmentation.generate\_prompt(query, chunks)**

**\# Gerar resposta**

**response \= generation.generate(prompt)**

**print(response)**

Se você quiser saber algo sobre os datasets sintéticos, agora você pode escrever a query em "pt-br"

**query \= "O que é dataset sintético?" dataset \= AgentRAGemini().query(query)**

**dataset\_escolhido \= dataset\[’dataset\_name’\]**

E a saída será um texto voltado para esse assunto. Legal, né?

**4.7 EXERCÍCIOS**

1. Explique, com suas próprias palavras, qual a principal diferença entre um RAG tradicional e o AgenticRAG.  
2. Use a analogia do guarda de trânsito apresentada no capítulo para justificar como o AgenticRAG atua no direcionamento do fluxo de informações.  
3. Analise a importância da classe **Datasets**. Por que ela é fun- damental para que o agente consiga decidir qual base vetorial deve ser consultada?  
4. Imagine que você deseja adicionar um novo dataset sobre saúde. Escreva como esse dataset deveria ser registrado na classe **Datasets**, incluindo o nome, a descrição e o locale.  
5. Reflita sobre o papel da classe **AgentRAGAbstract**. Por que ela é declarada como uma classe abstrata e o que isso garante na arquitetura do RAG?  
6. Explique como o método **create\_prompt** da classe **AgentRAGe- mini** contribui para que a resposta esteja sempre padronizada no formato JSON.  
7. No fluxo do AgenticRAG, em qual momento ocorre a decisão sobre qual dataset será usado? Descreva passo a passo como essa escolha é realizada.  
8. Analise as vantagens de usar o framework **CrewAI** para criar  
9. 

agentes, em comparação com a chamada direta à API de uma LLM.

10. No código da "main", identifique o papel de cada uma das três classes principais: **Retriever**, **Augmentation** e **Generation**. Explique como elas se complementam no fluxo.  
11. Proponha um cenário prático em que o AgenticRAG poderia ser aplicado em sua área de interesse, explicando como o agente escolheria o dataset adequado e quais etapas do fluxo seriam mais relevantes.  
12. Essa agora é **hard**. E se você quisesse usar uma ferramenta de busca na web ao invés de usar os chunks do **Retriever** para enviar ao **Generation**, o que você faria?  
13. 

**CAPÍTULO	5**  
O RAG em Grafos: GraphRAG

Imagine que vocês estão lendo uma coleção enorme de livros, mas alguém rasgou as páginas e misturou tudo em uma caixa. O RAG tradicional é como tentar responder a perguntas puxando algu- mas páginas que ’parecem’ certas e montando a ideia no improviso. O GraphRAG convida vocês a fazer algo mais inteligente: antes de responder, organizar a biblioteca por temas e conexões, como quem cria um mapa mental do acervo.

Vocês já viram como o RAG pode ser ótimo quando a resposta está bem ’localizada’ em poucos trechos, mas também como ele pode se tornar frágil quando a pergunta pede uma visão mais ampla, juntando pistas espalhadas pelo corpus. Quando vocês dependem apenas de recuperar textos soltos, vocês ficam reféns de escolhas como os **top\_k** chunks mais relevantes. Isso não é ’errado’; só tem um limite natural: há perguntas que não querem apenas um trecho bom; querem contexto estrutural, relações e consistência entre partes distantes. O GraphRAG entra exatamente para ajudar vocês a dar um enfoque global nas respostas.

Pensem em perguntas como: ’Quais são os principais temas deste livro?’ e ’Como o conhecimento do capítulo 1 se relaciona com o conhecimento do capítulo 9?’. É aqui que o GraphRAG começa a brilhar: ele empurra o raciocínio para a estrutura do corpus, em vez de depender apenas de pedaços isolados.

Pensem no GraphRAG como um modo de organizar o conheci- mento antes de interagir com ele. Em vez de tratar o corpus como

uma pilha de pedaços desconectados, vocês passam a tratá-lo como um conjunto de elementos que se relacionam, principalmente quando existem informações relacionadas, mas espalhadas em trechos muito distantes uns dos outros.

**Link do projeto GraphRAG:**

[https://bit.ly/graphrag-sandeco](https://bit.ly/graphrag-sandeco)

**5.1 DO VETOR AO GRAFO**

Vocês conhecem muito bem vetores e embeddings. Pensem assim: o vetor ajuda a descobrir *o que parece com o que*. Vocês fazem uma pergunta, calculam a similaridade, pegam os trechos mais próximos e seguem o jogo. Isso resolve muita coisa, especialmente quando o conhecimento está bem descrito em texto e a resposta cabe em poucos pedaços.

Só que existe um tipo de pergunta em que ’parecido’ não basta: vocês precisam entender *quem está ligado a quem*, *por qual motivo* e *em qual contexto*. É aqui que o grafo entra como uma estrutura de raciocínio mais natural para capturar globalidade e dependência. Usem um grafo como se usa um mapa: ele não tenta resumir tudo em um número (como o vetor); ele explicita conexões. Façam a analogia correta: embedding é ótimo para proximidade semântica; o grafo é ótimo para globalidade e dependência. Um não substitui o outro; eles se complementam.

**5.2 DEFINIÇÃO DE GRAFO**

Um grafo é uma forma de representar coisas e ligações entre elas. Ele é composto por **’nós’**, que são as ’coisas’ do seu problema, e por **arestas**, que são as ligações entre essas coisas. Um grafo também pode ter **propriedades**, que são informações extras colocadas nos

**’nós’** e/ou nas **arestas**, como nome, tipo, data ou um valor numérico.

Sei que o termo ’coisas’ é abstrato; então, vamos começar com o exemplo mais clássico possível: coisas são cidades e ligações são estradas entre cidades.

**Exemplo clássico de grafos**

Um exemplo clássico do uso de grafos é modelar capitais como nós e as distâncias rodoviárias entre elas como arestas ponderadas (o peso é a distância em km).

| Origem | Destino | Distância (km) |
| :---- | :---- | ----- |
| São Paulo | Rio de Janeiro | 439 |
| São Paulo | Curitiba | 403 |
| São Paulo | Belo Horizonte | 586 |
| Rio de Janeiro | Belo Horizonte | 445 |
| Rio de Janeiro | Curitiba | 829 |
| Belo Horizonte | Goiânia | 887 |
| São Paulo | Goiânia | 927 |
| Goiânia | Brasília | 204 |

**Tabela 5.1:** Arestas (estradas) e pesos (distâncias) em um grafo simples de capitais.

Agora vamos forçar uma regra aqui (ela não é real): para chegar a Brasília, tem que passar por Goiânia. Para isso, não criem arestas diretas de qualquer capital até Brasília. Assim, Brasília fica conectada apenas a Goiânia, e qualquer caminho que termine em Brasília passa obrigatoriamente por Goiânia.

Transformando esses dados em grafo, teremos:

Figura 5.1: Grafo de capitais com **nós**, **arestas** e **pesos** (km), destacando a regra forçada de que ’Brasília’ se conecta apenas a ’Goiânia’.

A Figura [5.1](#bookmark=id.76nxfm936rjs) mostra os dados visualmente em um grafo. Vamos

ler assim: cada círculo é um **nó** (uma capital) e cada linha é uma **aresta** (uma ligação rodoviária). Em seguida, vamos interpretar os valores em ’km’ como **propriedades** da aresta, isto é, um **peso** que quantifica o custo de percorrer aquela conexão. Vamos apontar para ’São Paulo’ e seguir as arestas que saem dele; depois, vamos fazer o mesmo com ’Goiânia’ e perceber que ela conecta com ’São Paulo’, com ’Belo Horizonte’ e, principalmente, com ’Brasília’. Essa leitura fixa o trio ’nó–aresta–peso’ e treina vocês para pensar em estrutura, não apenas em proximidade.

Agora vamos aplicar a regra forçada diretamente na figura: como ’Brasília’ só encosta em ’Goiânia’, qualquer trajeto até ’Brasília’ é obrigado a passar por ’Goiânia’.  Vamos fazer uma conta simples e ver o efeito do **peso**: sigam ’São Paulo’ *→* ’Goiânia’ (927 km) e depois ’Goiânia’ *→* ’Brasília’ (204 km), somando 1131 km; em seguida, comparem com um caminho alternativo que passa por ’Belo Horizonte’, somando 586 km \+ 887 km \+ 204 km. Guardem esse hábito: olhem a estrutura, sigam as conexões e somem pesos para justificar por que um caminho é melhor que outro. Essa disciplina de justificativa por relações explícitas é a mudança mental que interessa antes das próximas etapas.

**5.3 DE TEXTOS PARA GRAFOS**

Ok, aqui vocês devem estar pensando: ’Caramba, Sandeco, mas a gente não usa apenas tabelas como fonte; também usamos textos ou partes deles’. Perfeito. Agora é a virada de chave: a partir de um texto, vamos identificar as entidades que realmente importam, conectar essas entidades por meio de relações explícitas e observar como o resultado deixa de ser apenas ’um conjunto de trechos’ e se torna uma estrutura navegável. Nesta seção, transformamos texto em grafo e validamos, na prática, se conseguimos identificar ligações consistentes entre partes distantes do conteúdo.

Agora, vamos fazer o exercício com duas frases simples.

**FRASE 1**: Sandeco ensina IA e escreveu um livro sobre RAG.

**FRASE 2**: Sandeco é casado com Etiene.

**Padrões e definições**

Antes de extrair qualquer coisa, vamos adotar um padrão de consistência: vamos escrever o **TIPO** da entidade em maiúscu- las (PESSOA, TECNOLOGIA, OBRA) e também vamos escrever o **TIPO** da relação em maiúsculas (ENSINA, ESCREVEU, E\_SOBRE, E\_CASADO\_COM). Vamos manter o nome da entidade como apa- rece no texto (com ajustes mínimos quando existir ’\_’).

**Entidades**

Vamos separar o que é **entidade** e o que é **relação**. As **proprie- dades** também importam para rastreabilidade e auditoria, mas vamos deixá-las para mais adiante, quando vocês já estiverem confortáveis com a ideia de **nós** e **arestas**.

**Entidade	Tipo**

Sandeco	PESSOA

Etiene	PESSOA

IA	TECNOLOGIA

RAG	TECNOLOGIA

Livro\_sobre\_RAG	OBRA

**Tabela 5.2:** Entidades extraídas e seus tipos (tipo em maiúsculas como padrão).

Transformando as **entidades** em grafo, a visualização fica assim:

Figura 5.2: Entidades extraídas das frases, representadas como **nós**.

**Relações**

Ok, agora vamos extrair as relações entre as entidades. Essas relações serão as **arestas** que conectam os **nós**.

| Entidade | Relação | Entidade alvo |
| :---- | :---- | :---- |
| Sandeco Sandeco Livro\_sobre\_RAG Sandeco | ENSINA ESCREVEU E\_SOBRE E\_CASADO\_COM | IA Livro\_sobre\_RAG RAG Etiene |

**Tabela 5.3:**  Relações extraídas (tipo em maiúsculas como padrão) como arestas entre entidades.

Adicionando as arestas ao grafo, a visualização fica assim:

Figura 5.3: Grafo com **nós** (entidades) e **arestas** (relações) extraídos das frases.

Feita essa primeira leitura, o próximo passo é salvar esse grafo em um banco para consultar, evoluir e versionar com consistência. É aqui que o Neo4j entra: ele vai guardar **nós** e **arestas**, e mais adiante, vamos enriquecer isso com **propriedades** para rastreabilidade e auditoria.

**5.4 NEO4J**

Para armazenar um grafo de forma útil, vocês precisam de um lu- gar onde **nós** e **arestas** não sejam apenas uma estrutura temporária em memória, mas sim dados persistentes, consultáveis e fáceis de inspecionar. É exatamente isso que um **banco de dados de grafos** entrega: ele guarda as entidades e as conexões como elementos centrais e permite que vocês consultem o conhecimento seguindo relações, detectando caminhos e validando padrões de ligação. Em vez de reconstruir o ’quem se conecta com quem’ a cada execução, vocês passam a consultar a estrutura pronta, navegando pelo grafo e justificando resultados com base em conexões explícitas. As **pro- priedades** entram como um enriquecimento natural, adicionando metadados e evidências em **nós** e **arestas**, mas vamos aprofundar esse ponto mais adiante, quando a base de entidades e relações já estiver bem firme.

Nesse capítulo, o banco escolhido para persistir e consultar esse grafo será o Neo4j. Ele será usado para armazenar o que extraímos do texto e, principalmente, para permitir consultas por padrões de conexão de um jeito direto e visual. A partir daqui, o grafo deixa de ser apenas uma visualização e passa a funcionar como um índice: vocês salvam **nós** e **arestas**, inspecionam a estrutura, executam queries e iteram até a modelagem ficar consistente. Essa etapa remove a sensação de ’grafo mágico’, porque tudo fica verificável: o que foi criado, como foi ligado e como pode ser consultado, preparando o terreno para as próximas etapas do pipeline.

**5.5 INSTALANDO O NEO4J NO DOCKER**

Para instalar a o Neo4J no Docker, usaremos a versão **Enter- prise**, o que amplia as capacidades do sistema e permite recur- sos necessários para implementações de **GraphRAG** com suporte

vetorial e processamento otimizado. Essa versão roda a imagem **’neo4j:5.21.0-enterprise’** e adiciona novos parâmetros no *docker- compose*, especialmente a aceitação da licença de desenvolvedor e a desativação da validação estrita de configuração, que costuma ser necessária quando vocês adicionam componentes de vetorização e integrações externas.

No bloco **’environment’**, o parâmetro **’NEO4J\_ACCEPT\_LICENSE\_AGREEME**

definido como yes indica que vocês aceitam automaticamente os termos da licença de desenvolvedor. Essa licença é chamada oficial- mente de **Neo4j Enterprise Developer License** e permite uso local para pesquisa, ensino e desenvolvimento experimental, desde que vocês não implantem o sistema em produção comercial.

Além da aceitação da licença, existe uma variável importante:

## **’NEO4J\_server\_config\_strict\_**	**alidation\_enab**

 **led’** definida

como False no texto explicativo (no arquivo de configuração ela apa- rece como ’false’). Ela desativa a validação rígida das configurações internas, o que costuma ser necessário para que o módulo veto- rial em cenários de **GraphRAG** funcione sem bloquear parâmetros adicionais.

**Link do projeto GraphRAG:**

[https://bit.ly/graphrag-sandeco](https://bit.ly/graphrag-sandeco)

A estrutura do *docker-compose* completo para a versão Enterprise fica assim:

**services: neo4j:**

**image: neo4j:5.21.0-enterprise container\_name: neo4j-enterprise restart: unless-stopped**

**ports:**

**\- "7474:7474"	\# Web Browser**

**\- "7687:7687"	\# Bolt protocol environment:**

**\#	Autenticacao**  
**NEO4J\_AUTH: neo4j/sandeco123 \#altere a senha**

**\#	Aceita automaticamente a licenca Developer (uso gratuito local)**  
**NEO4J\_ACCEPT\_LICENSE\_AGREEMENT: "yes"**

**\#	Ativa plugins essenciais**  
**NEO4J\_PLUGINS: ’\["apoc", "graph-data-science**

**"\]’**

**\# Configuracoes de memoria (ajuste conforme sua maquina)**  
**NEO4J\_server\_memory\_heap\_initial**	**size: 1G**

**NEO4J\_server\_memory\_heap\_max**	**size: 2G NEO4J\_dbms\_memory\_pagecache\_size: 1G**

**\#	Permite import/export via APOC NEO4J\_apoc\_export\_file\_enabled: "true" NEO4J\_apoc\_import\_file\_enabled: "true" NEO4J\_apoc\_import\_file\_use**	**neo4j**	**config: "**

**true"**

**\#	Config extra**

**NEO4J\_server\_config\_strict**	**validation\_enabled: "false"**  
**volumes:**

- **./data:/data persistente**  
- **./logs:/logs**  
- **./import:/import importacoes**  
- **./plugins:/plugins APOC, GDS)**

**networks:**

- **neo4jnet**

**\#**  
**Banco de dados**  
**\#**  
**Pasta para LOAD CSV /**  
**\#**  
**Plugins instalados (**  
**networks:**

**neo4jnet: driver: bridge**

Em resumo: vocês podem usar essa versão Enterprise localmente para pesquisa, ensino e desenvolvimento experimental. Se o projeto evoluir para uma aplicação comercial em produção, aí sim será necessário obter uma licença paga junto à Neo4j Inc.

**Instalando**

Execute o comando abaixo na mesma pasta onde está o arquivo **docker-compose.yml** para subir o Neo4j em segundo plano. Em seguida, acessem **http://localhost:7474** e façam login com usuá- rio **neo4j** e senha **sandeco123**, exatamente como foi definido no compose.

**docker compose up \-d**

**5.6 CYPHER: CONVERSANDO COM O GRAFO**

Pensem no Cypher como um ’GPS do grafo’. Se o grafo é o mapa com **nós** e **arestas**, o Cypher é a linguagem que vocês usam para dizer: ’criem este lugar’, ’liguem estes pontos’ e, só depois, ’me mostrem como isso ficou’. Em vez de escrever consultas pensando em tabelas, vocês descrevem padrões de conexão: um **nó** ligado a outro **nó** por uma **aresta** com um tipo específico. O ganho de fluência vem do fato de que vocês escrevem o padrão de forma visual, e o banco persiste exatamente essa estrutura.

Para criar entidades no Neo4j utilizando a linguagem Cypher, utili- zem as cláusulas **CREATE** ou **MERGE**, escrevendo os **nós** entre pa- rênteses. Enquanto o **CREATE** gera sempre um novo nó (permitindo múltiplas instâncias), o **MERGE** funciona como um ’get-or-create’, criando a entidade apenas se não existir um padrão idêntico de ró- tulos e propriedades. Na prática de modelagem, a sintaxe básica segue este padrão:

**CREATE/MERGE (n:ROTULO {propriedade: ’valor’})**

Priorizem o uso do **MERGE** para entidades que não podem ser duplicadas (como um CPF ou um ID único) e reservem o **CREATE** para quando a intenção for explicitamente adicionar um novo registro, independentemente de existências prévias. Observem a diferença em exemplos mínimos:

**\# CREATE: sempre cria um novo nó**

**CREATE (p:PESSOA {cpf: ’00000000000’, nome: ’**

**Fulano’});**

**\# MERGE: cria apenas se nao existir um nó com o mesmo padrao**

**MERGE (p:PESSOA {cpf: ’00000000000’, nome:’Fulano’**

**});**

Para criar relacionamentos em Cypher, utiliza-se a mesma sintaxe de setas direcionais que visualmente representam a conexão entre dois nós, geralmente dentro de uma cláusula MATCH (para encontrar nós existentes) ou MERGE. A estrutura básica segue o padrão:

**(a)-\[:NOME\_RELACIONAMENTO {propriedade: ’valor’**

**}\]-\>(b)**

Os colchetes definem o tipo do vínculo e podem conter proprie- dades específicas, como a data de nascimento ou o peso de uma transação. Assim como na criação de nós, recomenda-se o uso do MERGE para evitar a duplicidade de conexões entre as mesmas entidades, garantindo que o grafo mantenha a integridade semântica ao conectar os pontos de dados de forma única e direcionada.

**Criando as entidades das Frases de exemplo**

Agora aplicaremos esse padrão ao nosso exemplo das Frases 1 e 2\. Aqui a recomendação é a mesma: usem **MERGE** para evitar duplicação e mantenham os rótulos em maiúsculas (PESSOA, TEC- NOLOGIA, OBRA). Notem também o detalhe de consistência: a obra foi padronizada como ’Livro\_sobre\_RAG’, e esse mesmo nome deve aparecer de forma idêntica em toda a modelagem.

**MERGE (s:PESSOA {nome: ’Sandeco’}) MERGE (e:PESSOA {nome: ’Etiene’}) MERGE (ia:TECNOLOGIA {nome: ’IA’}) MERGE (rag:TECNOLOGIA {nome: ’RAG’})**  
**MERGE (l:OBRA {nome: ’Livro\_sobre\_RAG’});**

Depois de executar o bloco acima, façam uma verificação imediata no Neo4j Browser para confirmar que os **nós** foram criados. Abram o Browser, escrevam uma query geral que liste os **nós** existentes e executem para visualizar o grafo. Observem que, neste momento, vocês ainda verão apenas **nós** isolados, porque as **arestas** ainda não foram criadas; essa checagem separa ’criação de entidades’ de ’criação de relações’ e evita confusão no diagnóstico.

**MATCH (n) RETURN n;**

Figura 5.4: Entidades salvas no Neo4J

Agora vamos ligar essas **entidades**. Para manter o grafo determi- nístico, localizaremos os nós e criaremos as **arestas** com **MERGE**, evitando duplicação.  Façam isso como hábito:  primeiro localizem o que vai ser conectado; depois conectem com o tipo correto da relação.

**MATCH (s:PESSOA {nome: ’Sandeco’}), (ia:TECNOLOGIA**

**{nome: ’IA’})**

**MERGE (s)-\[:ENSINA\]-\>(ia);**

**MATCH (s:PESSOA {nome: ’Sandeco’}), (l:OBRA {nome:**

**’Livro\_sobre\_RAG’})**

**MERGE (s)-\[:ESCREVEU\]-\>(l);**

**MATCH (l:OBRA {nome: ’Livro\_sobre\_RAG’}), (rag: TECNOLOGIA {nome: ’RAG’})**  
**MERGE (l)-\[:E\_SOBRE\]-\>(rag);**  
**MATCH (s:PESSOA {nome: ’Sandeco’}), (e:PESSOA {**

**nome: ’Etiene’})**  
**MERGE (s)-\[:E\_CASADO\_COM\]-\>(e);**

Só depois de criar é que faz sentido validar. Para conferir se o subgrafo foi persistido como vocês esperavam, busquem as conexões e devolvam **nós** e **arestas** para o Neo4j Browser renderizar.

**MATCH (n) RETURN n;**

Figura 5.5: Agora nosso grafo completo

**5.7 MICROSOFT GRAPHRAG**

A Microsoft foi quem criou a ideia do GraphRAG com extração au- tomática de entidades e relacionamentos como base de um pipeline completo que sai do texto e chega a uma estrutura navegável. No ar- tigo ’From Local to Global: A GraphRAG Approach to Query-Focused Summarization’, a proposta é simples de entender e poderosa na prática: em vez de depender apenas da recuperação vetorial de trechos soltos, vocês constroem um grafo de conhecimento a partir do corpus, organizam esse grafo em comunidades e pré-produzem resumos por comunidade, criando um índice que representa o corpus de forma mais estrutural.

Veja como funciona de forma resumida a sequencia de execução do GraphRAG da Microsoft na Figura [5.6.](#bookmark=id.sf58yrbkmdws) Primeiro, leiam o diagrama como dois tempos diferentes do mesmo sistema: à esquerda está o **tempo de indexação** (preparação do conhecimento) e à direita está o **tempo de consulta** (resposta à pergunta). Neste ponto do capítulo, foquem deliberadamente nas caixas destacadas em verde, porque elas representam o que muda na prática quando vocês saem do RAG tradicional e entram no GraphRAG: a resposta deixa de nascer diretamente de **top\_k** chunks e passa a nascer de uma estrutura intermediária já organizada em comunidades e resumos.

Agora sigam a sequência da direita, de baixo para cima, como se estivessem executando o sistema. Comecem nas **Comunidades do grafo**: vocês podem imaginar que o corpus foi organizado em grupos de entidades fortemente conectadas, e cada grupo representa um tema ou subtema. Em seguida, olhem para **Resumos da comuni- dade** e entendam o papel desse artefato: antes mesmo da pergunta existir, o sistema produz uma síntese personalizada para o domínio, que descreve o que aquela comunidade ’sabe’ de forma compacta e consultável. Quando vocês fazem uma pergunta, o GraphRAG não tenta responder juntando pedaços soltos; ele primeiro produz **Respostas da comunidade**, isto é, respostas parciais geradas a

Figura 5.6: Pipeline do GraphRAG da Microsoft, separando tempo de indexação e tempo de consulta, com destaque para a sequência de consulta: comunidades do grafo, resumos da comunidade, respostas da comunidade e resposta global.

partir das comunidades mais relevantes para a consulta. Por fim, ele consolida essas respostas parciais em uma **Resposta global** por meio de sumarização focada na consulta, garantindo cobertura e consistência entre partes distantes do corpus. Fixem esta leitura: a resposta global não é um trecho recuperado, é uma agregação orientada por estrutura.

Para internalizar a lógica, façam um exercício prático sempre que olharem para esse pipeline: escrevam uma pergunta global, apontem no diagrama onde ela entra (na fase de consulta) e acompanhem mentalmente como ela sobe de **Comunidades do grafo** para **Re- sumos da comunidade**, depois para **Respostas da comunidade** e finalmente para **Resposta global**. Quando vocês repetirem esse caminho algumas vezes, vocês param de tratar o GraphRAG como ’mágica’ e passam a enxergar o que ele realmente é: um processo controlável de seleção de comunidades e consolidação de respostas, que existe justamente para lidar com perguntas que exigem visão global e relações entre partes distantes do texto.

**5.8 EXTRAÇÃO AUTOMÁTICA DE ENTIDADES E RELACIONAMENTOS**

Pensem na extração como montar um ’jogo de etiquetas’ antes de organizar um armário: se vocês não sabem quais categorias existem no armário, vocês vão colar etiquetas aleatórias e misturar coisas que não deveriam estar juntas. Aqui, o grande segredo não é só ’usar uma LLM’, e sim conhecer bem o corpus. Sem conhecer o cor- pus, vocês não conseguem direcionar a LLM para extrair entidades que realmente importam e relações que fazem sentido nos textos; o resultado vira ruído, com entidades genéricas demais, relações inconsistentes e um grafo que parece bonito, mas não representa o conhecimento do material. Por isso, antes de pedir que a LLM extraia entidades e relacionamentos, definam muito bem quais **TIPOS** de entidade e quais **TIPOS** de relacionamento são possíveis em todo o corpus.

Isso é importante por três razões práticas. Primeiro, vocês re- duzem ambiguidade: a LLM deixa de inventar rótulos, sinônimos e relações redundantes, porque ela passa a operar dentro de um voca- bulário fechado. Segundo, vocês aumentam consistência: a mesma coisa no texto vira sempre o mesmo tipo (PESSOA, TECNOLOGIA, OBRA), e a mesma ação vira sempre o mesmo relacionamento (EN- SINA, ESCREVEU, E\_SOBRE, E\_CASADO\_COM), o que evita que o grafo exploda em variações do mesmo conceito.

**{**  
**"tipos\_entidade": { "PESSOA": 2,**

**"TECNOLOGIA": 2,**

**"OBRA": 1,**

**"LOCALIDADE": 1,**

**"DADO": 1**

**},**  
**"tipos\_relacionamento": { "ENSINA": 1,**

**"ESCREVEU": 1,**  
**"E\_SOBRE": 1,**  
**"E\_CASADO\_COM": 1**

**}**

**}**

Terceiro, vocês tornam o pipeline auditável: quando alguém olha o grafo, fica claro quais tipos existem e quais relações são permitidas, e isso facilita a depuração de extrações erradas. Usem o exemplo abaixo como modelo:  ele fixa, de forma explícita, os **TIPOS** que a LLM deve usar. Notem que esse JSON representa exatamente as duas frases do capítulo: ele permite modelar PESSOA, TEC- NOLOGIA e OBRA, e permite exatamente os relacionamentos que conectam ’Sandeco’, ’IA’, ’Livro\_sobre\_RAG’, ’RAG’ e ’Etiene’.

**5.9 GERANDO COMUNIDADES NO NEO4J**

Imagine que o grafo é uma cidade gigantesca vista de cima, cheia de ruas e vielas ligando pessoas, lugares e assuntos. Se você tenta entender essa cidade olhando rua por rua, você se perde; mas se você identifica os bairros, tudo fica óbvio: cada bairro tem sua ‘cara’, seus hábitos e seus temas. Gerar comunidades no Neo4j é exatamente isso: mandar o algoritmo passear pela cidade e marcar onde estão os bairros naturais, isto é, os grupos de **nós** que se conectam fortemente entre si e bem menos com o resto. Depois que você enxerga os bairros, você para de navegar no improviso e começa a raciocinar por blocos: ‘qual comunidade explica essa pergunta?’, ‘quais comunidades se conversam?’, ‘qual é o caminho mais curto entre dois temas?’.

**O Algoritmo de Leiden**

O **algoritmo de Leiden** encontra comunidades em grandes redes, como nos grafos. Ele separa os **nós** em grupos *sem sobreposição*, de modo a maximizar a modularidade. A modularidade mede a qualidade dessa separação: ela compara o quanto os **nós** dentro de um mesmo grupo estão bem conectados entre si com o quanto estariam conectados se a rede fosse aleatória.

Ele trabalha de forma hierárquica: melhora a modularidade de maneira gulosa, depois junta cada comunidade e a transforma em um único nó, criando um grafo menor (condensado). Em seguida, repete o mesmo processo nesse grafo condensado. O algoritmo de Leiden é uma melhoria do algoritmo de Louvain e resolve um problema importante: às vezes, o algoritmo de Louvain cria comunidades que parecem boas em termos de pontuação, mas ficam mal conectadas internamente. Para evitar isso, o Leiden faz refinamentos em etapas, quebrando comunidades de tempos em tempos em partes menores e bem conectadas, antes de continuar a otimização.

**5.9 A FUNÇÃO DO PESO NAS RELAÇÕES**

Imagine que o seu grafo é uma festa gigante, com muita gente conversando ao mesmo tempo. Cada **nó** é uma pessoa na festa, e cada **aresta** é uma conversa entre duas pessoas. Agora vem o detalhe que muda tudo: algumas conversas são fracas e rápidas, enquanto outras são profundas e frequentes. É exatamente isso que o **strength** representa: o volume da conversa, a intensidade do vínculo.

Quando você faz a projeção no GDS, é como pedir para o segu- rança copiar a planta da festa para uma prancheta, só para analisar o fluxo de conversa sem mexer na festa real. Em seguida, Leiden entra como um organizador esperto: ele anda pela festa procurando ’rodi- nhas’ naturais, isto é, grupos onde as pessoas conversam muito entre

si e bem menos com o resto do salão. Como ele trata as ligações como não direcionadas, ele ignora quem começou a conversa e foca apenas no fato de que existe conexão. E como ele usa o **strength** como peso, ele dá mais importância para conversas fortes e menos para conversas fracas. No final, ele cola uma etiqueta communityId na testa de cada pessoa, dizendo a qual rodinha ela pertence.

**Cypher das comunidades**

**\#antes de criar a projeção**  
**CALL gds.graph.drop(’graphrag\_all’, false);**

**MATCH (source)-\[r\]-\>(target) RETURN gds.graph.project(**  
**’graphrag\_all’,**

**source, target,**

**{ relationshipProperties: r { .strength } },**

**{ undirectedRelationshipTypes: \[’\*’\] }**  
**);**

**CALL gds.leiden.write(’graphrag\_all’, { writeProperty: ’communityId’, relationshipWeightProperty: ’strength’, randomSeed: 19**

**});**

A primeira coisa que você precisa fazer aqui é preparar um re- gistrador de datasets da forma mais prática possível: garanta que o estado anterior não esteja contaminando o experimento, recrie a projeção do grafo com os pesos corretos e, só então, rode o algo- ritmo que vai escrever a comunidade em cada nó. Faça isso com

disciplina: elimine a projeção antiga para não reutilizar um snapshot desatualizado, projete o grafo novamente, trazendo a propriedade **strength** como peso, e execute o Leiden para gravar o communityId diretamente no banco. Assim, você deixa o resultado persistido e pronto para ser consultado no restante do pipeline, sem depender de memória.

Comece derrubando a projeção anterior com gds.graph.drop. Execute esse comando antes de criar a nova projeção porque o GDS mantém grafos projetados em memória com nomes e, se você tentar criar novamente com o mesmo nome, poderá ocorrer um conflito ou, pior, você pode achar que está analisando o grafo atual quando, na verdade, está reutilizando um snapshot antigo. Escreva false no segundo parâmetro para controlar o comportamento de liberação e evitar que o procedimento tente apagar coisas fora do escopo do catálogo do GDS; entenda que esse passo remove apenas o grafo projetado, não apaga os seus nós e relacionamentos no Neo4j.

Em seguida, projete o grafo com gds.graph.project.  Faça a leitura desse trecho como ’carregue em memória um grafo cha- mado graphrag\_all usando os nós e arestas do meu banco’. Use o MATCH (source)-\[r\]-\>(target) para alimentar o procedimento com todas as ligações do seu grafo, mas peça explicitamente para levar junto a propriedade **strength** de cada relação, porque você vai usar esse valor como peso no Leiden. Note que, no bloco relationshipProperties, você está dizendo ao GDS para tra- zer strength para dentro do grafo projetado; sem isso, você até conseguiria rodar o algoritmo, mas não conseguiria ponderar as conexões como você planejou.

Ainda na projeção, mantenha undirectedRelationshipTypes: \[’\*’\] para tratar todas as relações como não direcionadas. Faça isso porque, na detecção de comunidades, o que importa é a intensi- dade da ligação entre os nós e não o sentido da seta; você quer que a conexão conte dos dois lados na hora de formar ’bairros’ de nós fortemente conectados.

Por fim, execute gds.leiden.write. Aqui você vai mandar o Leiden calcular as comunidades no grafo projetado graphrag\_all e

gravar o resultado nos nós do seu banco. Escreva writeProperty: ’communityId’ para definir o nome do campo persistido,  e es- creva relationshipWeightProperty:	’strength’ para forçar o algoritmo a usar o peso das relações.		Fixe isso:  sem **relati- onshipWeightProperty**, o Leiden trata todas as arestas como se tivessem a mesma força, e você perde exatamente a nuance que modelou com **strength**. Defina também randomSeed:	19 para tor- nar o resultado reprodutível; faça isso porque algoritmos com etapas estocásticas podem variar entre execuções, e você quer consistência ao depurar comunidades ou comparar versões do grafo.

**Listar Comunidades**

Vamos ver quantas comunidades foram geradas e quantos nós existem em cada uma delas. Execute a consulta abaixo para agrupar os nós pelo communityId e contar quantos elementos caíram em cada comunidade, retornando apenas duas colunas simples: id e entities. Ordene por id para ler do menor para o maior.

**MATCH (n)**

**WHERE n.communityId IS NOT NULL**

**WITH n.communityId AS id, count(n) AS entities RETURN id, entities**

**ORDER BY id**

Rodando o script no Neo4J, temos um resumo direto do particio- namento gerado pelo Leiden: a tabela lista cada comunidade pelo campo id e a quantidade de nós associados a ela em entities, mostrando que o grafo foi separado em quatro comunidades com tamanhos 7 (id 1), 7 (id 2), 6 (id 3\) e 2 (id 4). Use essa visão como um ’mapa de entrada’ do seu índice comunitário, porque ela te diz quan- tos elementos você vai recuperar quando filtrar por communityId e te ajuda a decidir, no pipeline, quantas comunidades vale a pena inspecionar primeiro. Guarde isso, porque esse resultado será impor- tante no Python: você vai iterar pelos ids, buscar os nós e arestas de cada comunidade, gerar resumos por comunidade e navegar nesse conjunto de comunidades como camadas de contexto para responder perguntas de forma estruturada.

**5.10 MOSTRANDO OS GRAFOS DA COMUNIDADE**

Agora que temos os identificadores das comunidades, faça uma consulta que mostre o subgrafo de uma comunidade específica para que você possa enxergar, de forma concreta, quais entidades fica- ram agrupadas juntas.  Execute o MATCH (n)-\[r\]-(m) para cap-

turar pares de nós conectados por uma aresta e filtre com WHERE n.communityId \= 1 AND m.communityId \= 1 para manter ape- nas as conexões em que os dois extremos pertencem à mesma comunidade. Use o número 3 como exemplo e substitua pelo communityId que você quiser inspecionar.

**MATCH (n)-\[r\]-(m)**

**WHERE n.communityId \= 1 AND m.communityId \= 1 RETURN n, r, m;**

Em seguida, retorne n, r, m para que o Neo4j Browser rende- rize visualmente os nós e as arestas internas daquela comunidade. Faça essa inspeção como um teste de sanidade: você confirma se as entidades dentro do grupo realmente compartilham ligações relevantes e percebe rapidamente se a comunidade está ’coesa’ ou

se os nós estão mais conectados para fora do grupo do que en- tre si. Quando você consolidar essa leitura, comece a usar essas comunidades como unidades de navegação no pipeline: selecione uma comunidade, recupere suas entidades e relações, e utilize esse subgrafo como contexto estruturado para as próximas etapas em Python.

Figura 5.7: Comunidades no Neo4J

A Figura [5.8](#bookmark=id.ix1udivr2snu) mostra o resultado do particionamento em comuni- dades que você gerou no Neo4j: o algoritmo agrupou o grafo em quatro comunidades, e cada grupo passou a representar um *assunto* dominante. A comunidade com communityId \= 1 ficou associada ao assunto ’Sandeco’, a comunidade communityId \= 2 ao assunto ’agentes’, a comunidade communityId \= 3 ao assunto ’grafo’ e a comunidade communityId \= 4 ao assunto ’Banco de dados’. Leia isso como um mapa temático do conhecimento: cada comunidade é um bloco coerente do corpus e os rótulos de assunto indicam, de forma resumida, sobre o que aquele bloco tende a responder quando você navegar ou recuperar contexto por comunidade no pipeline.

**5.11 GERANDO RESUMOS DAS COMUNIDADES**

Gerar os resumos das comunidades é o passo que transforma o particionamento do grafo em um artefato realmente utilizável no

pipeline: em vez de consultar milhares de conexões toda vez que fizer uma pergunta, você pré-condensa cada comunidade em um texto curto, denso e rastreável, capaz de representar o assunto domi- nante e as relações mais importantes daquele bloco. Faça isso de forma disciplinada: selecione uma comunidade pelo communityId, recupere um subconjunto representativo de entidades e relações (priorizando as conexões mais fortes e mais recorrentes) e envie esse contexto para a LLM gerar um resumo que funcione como ín- dice semântico. Em seguida, registre esse resumo no grafo para que ele possa ser recuperado rapidamente no momento da consulta, servindo como ponto de entrada para decidir quais comunidades me- recem aprofundamento quando a pergunta exigir uma visão global.

**A classe GraphQuery**

Use a classe GraphQuery como a interface central para traba- lhar com comunidades no grafo. Abaixo estão apenas os métodos públicos e a finalidade de cada um.

     **init ()** Inicializa o conector Neo4j e tenta inicializar a LLM (Generation) para geração de texto.

**list\_communities()** Lista as comunidades existentes e a conta- gem de entidades (nós) em cada comunidade.

**get\_community\_data(community\_id)** Lista os nós e os relacio- namentos de uma comunidade específica e retorna os dados em estrutura Python.

**get\_community\_details(community\_id, node\_limit, edge\_limit)**

Monta um payload estruturado em JSON com nós (priorizados e limitados por node\_limit) e arestas internas (priorizadas e limitadas por edge\_limit).

**generate\_community\_summary(community\_id, node\_limit, edge\_limit**

Gera um resumo da comunidade via LLM usando como entrada o JSON retornado por  
get\_community\_details.

**save\_community\_summary(community\_id, summary\_text)** Grava o resumo no Neo4j criando um nó (c:COMMUNITY) e um nó (s:SUMMARY), conectando-os por \[:HAS\_SUMMARY\] e atuali- zando c.currentSummaryId.

**get\_community(community\_id)** Lista a comunidade e o resumo atual associado por

currentSummaryId.

**list\_communities\_with\_summary()** Lista todas as comunidades com o texto do resumo atual.

**close()** Fecha a conexão com o banco por meio do conector.

**Executando a geração**

Vamos, então, realizar a geração e a gestão dos resumos das comunidades identificadas no grafo. Inicie o script importando o módulo json e a classe GraphQuery de seu pacote local. Em se- guida, instancie o objeto gq para estabelecer a comunicação com a estrutura de dados.

**import json**  
**from graph\_query.graph\_queries import GraphQuery**

**gq \= GraphQuery()**

Execute o método list\_communities() para recuperar todas as comunidades detectadas no processamento anterior e utilize uma função de impressão para verificar quantas foram encontradas. Este passo é essencial para garantir que a base de dados possui entidades agrupadas antes de iniciar a sumarização.

**print("\\n--- Listando Comunidades \---") communities \= gq.list\_communities() print(f"Comunidades encontradas: {len(communities)**

**}")**

Crie um laço de repetição para percorrer cada objeto dentro da lista de comunidades. Dentro deste loop, exiba o identificador da comunidade e as entidades que a compõem. Utilize o método generate\_community\_summary, passando o community\_id e os parâmetros de nível de detalhamento, para disparar a lógica de gera-  
ção de texto via LLM. Após gerar o resumo, invoque save\_community\_summary para persistir esse resultado no banco de dados, vinculando-o per- manentemente à sua respectiva comunidade.

**for community in communities: print(f"Comunidade: {community\[’id’\]},**

**Entidades: {community\[’entities’\]}") community\_id \= community\[’id’\]**

**summary \= gq.generate\_community\_summary( community\_id, 3, 6 )**

**print(summary)**

**saved\_result \= gq.save\_community\_summary( community\_id, summary)**

Finalize o processo recuperando a lista completa de resumos armazenados através do método list\_community\_summaries(). Percorra esses dados para validar se cada community\_id possui um id de resumo correspondente. Por último, chame obrigatoriamente o método close() para encerrar a conexão do objeto gq e liberar os recursos do sistema.

**resumos \= gq.list\_community\_summaries()**

**for resumo in resumos:**  
**print(f"Comunidade: {resumo\[’community\_id’\]}**

**\-------- \\n {resumo\[’id’\]}")**

**gq.close()**

**Visualizando as Comunidades**

Para visualizar as comunidades com seus resumos, vamos exe- cutar o seguinte script no Neo4J.

**MATCH (c:COMMUNITY)-\[r:HAS\_SUMMARY\]-\>(s:SUMMARY)**

**WHERE s.id \= c.currentSummaryId RETURN c, r, s;**

Rodando o código, as comunidades são:

Figura 5.8: Comunidades no Neo4J

**5.12 DETECÇÃO AUTOMÁTICA DE ENTIDADES**

O seu corpus é uma grande caixa de peças de LEGO misturadas: você até consegue montar algo olhando peça por peça, mas, sem separar por tipo, cor e encaixe, você perde tempo, repete trabalho e erra conexões óbvias. O artigo da Microsoft descreve o Graph- RAG como se as peças já estivessem catalogadas (entidades e relações prontas para formar comunidades e gerar resumos), mas, no mundo real, essa catalogação não cai do céu: ela precisa ser feita de modo consistente, repetível e auditável. Por isso, eu criei classes

em Python que atuam como uma ’triagem automática’: elas varrem os textos, detectam e normalizam entidades segundo um vocabulá- rio controlado, reduzem variações do mesmo conceito e devolvem um conjunto estruturado pronto para virar **nós** e **arestas** no Neo4j. O objetivo desta seção é mostrar como transformar texto cru em componentes bem definidos, pois é essa disciplina de extração que sustenta o resto do pipeline sem depender de improviso.

**Buscando Representatividade**

Quando o corpus é grande (pense em centenas de milhares ou milhões de textos), tentar ler tudo para definir **entidades** e **relacio- namentos** é inviável: você gastará tempo demais em redundância, pois muitos textos dizem a mesma coisa com pequenas variações. A saída prática é agrupar primeiro os textos com um algoritmo de clus- terização, de modo que cada cluster concentre itens semanticamente próximos e, em seguida, escolher apenas os textos mais represen- tativos de cada grupo (por exemplo, os mais centrais em relação ao centroide ou os que maximizam a cobertura de termos relevantes). Essa amostragem guiada por estrutura reduz o corpus a um conjunto pequeno, porém informativo, de exemplos que capturam os temas dominantes e as variações importantes de cada cluster. A partir desses representantes, você consegue desenhar um vocabulário de **TIPOS** e um conjunto inicial de padrões de relação que realmente aparecem no material, e só depois aplicar a extração automática em larga escala com muito menos ruído e muito mais consistência.

Para conseguir agrupar textos por *proximidade semântica*, preci- samos primeiro colocar todos no mesmo espaço de comparação: o espaço vetorial. Isso é exatamente o que vocês já fizeram no capítulo 2 no RAG tradicional: quebrar o texto em chunks e transformar cada chunk em um embedding, isto é, um vetor numérico que preserva similaridade de significado. Aqui a lógica é a mesma, só que com ou- tro objetivo: em vez de usar os vetores para recuperar **top\_k** trechos por consulta, vamos usar esses embeddings como base para clus-

terização. Na prática, vocês vetorizam **todos** os chunks do corpus, montam uma matriz de vetores e aplicam um algoritmo de clusteri- zação sobre esses pontos (os embeddings), de modo que chunks semanticamente próximos caiam no mesmo grupo. Só depois disso faz sentido falar em ’representatividade’: um cluster é um conjunto de vetores próximos, e os representantes são justamente os chunks mais centrais ou mais informativos dentro desse agrupamento.

Neste experimento, vamos usar três textos de assuntos diferentes que já estão na pasta docs dentro do projeto: Buraco\_negro.pdf, Estoicismo.pdf e Inflação.pdf.

**5.13 DEFININDO OS GRUPOS DE CHUNKS**

Vamos sair do modo ’pegar trechos no improviso’ e entrar no modo *de organizar primeiro para decidir melhor depois*. A ideia é simples: em vez de tratar cada chunk como uma unidade isolada, vamos formar **grupos semânticos** de chunks que falam de assuntos próximos, criando uma visão mais controlada do corpus. Para isso, vamos trabalhar em cima dos embeddings já armazenados em uma base persistente e, com eles, aplicar um processo de clusterização eficiente para separar o conjunto em clusters coerentes, cada um com seu centroide representando o ’miolo’ do tema. A partir desses grupos, deixamos de depender de leitura exaustiva e passamos a operar com amostras mais informativas, escolhidas de forma balan- ceada e reprodutível para guiar as próximas etapas do pipeline. O código abaixo você já conhece. Ele gera os embeddings dos chunks dos textos que estão armazenados na pasta ’docs’.

**from entities\_generation.semantic\_encoder import SemanticEncoder**  
**from entities\_generation.semantic\_clustering**

**import SemanticClustering**  
**from entities\_generation.schema\_builder import SchemaBuilder**

**\# 2\. Amostragem semântica collection \= "docs" encoder \= SemanticEncoder(**  
**docs\_dir="docs", \#diretório dos documentos**

**chunk\_size=500, \#tamanho do chunk overlap\_size=100, \#tamanho da sobreposição**

**)**

**\# Construir base vetorial**  
**stats \= encoder.build(collection\_name=collection)**

**\# Verificar se a coleção foi criada corretamente verificacao \= encoder.verify\_collection(**  
**collection\_name=collection)**

O ponto central aqui é que **grupo** não é um rótulo decorativo: ele se torna um mecanismo de controle de qualidade. Quando você define clusters e mede a representatividade por proximidade ao cen- troide, consegue selecionar um ’protótipo’ do cluster (o chunk mais central) e, ao mesmo tempo, trazer diversidade com alguns exemplos adicionais do mesmo grupo para não perder variações importantes do tema. Esse desenho cria um caminho prático para escalar: você organiza o espaço semântico com MiniBatchKMeans, obtém centroi- des e usa essa estrutura para amostrar de forma disciplinada o que realmente vale a pena inspecionar primeiro.

**K-means**

O *k-means* é um algoritmo de clusterização *não supervisionada* que separa um conjunto de pontos (no nosso caso, embeddings) em **k** grupos, tentando formar clusters internamente coesos e externa- mente separados. A ideia central é minimizar a soma das distâncias entre cada ponto e o **centroide** do cluster ao qual ele foi atribuído: quanto mais próximos os vetores estiverem do seu centroide, mais ’compacto’ fica o cluster e melhor o agrupamento segundo esse cri- tério. O algoritmo funciona como um ciclo de duas etapas que se repete até estabilizar: (1) **atribuição**, em que cada vetor é associado ao centroide mais próximo; (2) **atualização**, em que cada centroide é recalculado como a média (mean) de todos os vetores atribuídos a ele. Esse vai-e-volta continua até as atribuições não mudarem mais (ou até atingir um limite de iterações), resultando em **k** centroides e uma partição do espaço vetorial em **k** regiões.

Na prática, o que vocês ganham com isso é um mecanismo objetivo para dizer ’esses chunks falam de coisas parecidas’ sem precisar ler tudo: se dois chunks estão no mesmo cluster, é porque seus embeddings ficaram próximos no espaço semântico. E isso conecta diretamente com a nossa estratégia de representatividade: dentro de cada cluster, o chunk mais próximo do centroide tende a ser o mais ’típico’ daquele grupo, enquanto chunks mais distantes capturam variações e bordas do tema. A limitação é importante e vocês precisam internalizar: o k-means pressupõe clusters mais ou menos *globulares* (separáveis por distância) e exige que você escolha **k** antes de rodar; por isso, ele é excelente como ferramenta prática de organização e amostragem, mas não é uma ’verdade ontológica’ do corpus. Aqui, ele cumpre um papel objetivo: criar grupos semânticos úteis para reduzir o custo de inspeção e guiar a extração de entidades e relacionamentos com o mínimo de redundância.

Quando você aplica o K-means, observe que a figura está lhe mostrando uma transformação mental bem direta: antes, os chunks (os ícones de páginas) estão espalhados no plano como pontos sem

Figura 5.9: K-means antes e depois: chunks dispersos no espaço vetorial e, após o agrupa- mento, separados em clusters (grupos) que permitem amostragem representativa.

organização explícita. então, faça o seguinte exercício: olhe para o lado esquerdo e finja que cada página é um embedding de um chunk; depois, mova o olhar para o lado direito e veja o que o algoritmo faz por você — ele força uma partição do espaço em **k** grupos, isto é, ele pega pontos semanticamente próximos e os coloca no mesmo bloco visual, tornando o corpus navegável por **clusters**. Agora, foque nas áreas destacadas em verde (os grupos coloridos do lado direito): trate cada grupo como um **tema latente** e use isso para decidir a representatividade; em vez de ler tudo, clique mentalmente em um cluster e imagine que você vai escolher primeiro os chunks mais cen- trais desse grupo (os mais próximos do centro do aglomerado) para obter uma amostra que represente bem aquele tema. Em seguida, repita: pegue mais um ou dois chunks do mesmo cluster para cap- turar variações e só então passe para o próximo cluster, garantindo cobertura do corpus com custo controlado. Fixe esta regra: o lado direito da Figura [5.9](#bookmark=id.2vmdvfucqqcd) não está ’pintando’ páginas por estética; ele está lhe entregando uma estratégia operacional — agrupe, selecione representantes por proximidade interna e use esses representantes como base para extrair **entidades** e **relacionamentos** sem precisar inspecionar o corpus inteiro.

Para fazer a clusterização dos chunks basta rodar o código abaixo com a classe SemanticClustering.

**\#criar clusterização semântica**  
**clusterer \= SemanticClustering(collection\_name= collection)**

**ids, embeddings \= clusterer.get\_embeddings()**

**\#buscar amostras representativas sampled\_chunks \= clusterer.**  
**get\_representative\_samples(ids=ids,**

**embeddings=**

**embeddings, diversity\_per\_cluster=4)**

**clusterer.close()**

Nesse trecho, você executa o fluxo mínimo para sair de um cor- pus bruto e chegar a uma amostra pequena, porém informativa, pronta para inspeção e extração de **entidades** e **relacionamentos**. Primeiro, você instancia SemanticClustering apontando para a **collection\_name**, isto é, para a coleção onde os chunks já estão persistidos junto com seus embeddings; em seguida, ao chamar get\_embeddings(), você recupera dois artefatos fundamentais: ids (os identificadores dos chunks) e embeddings (os vetores que representam semanticamente cada chunk). Depois, você chama get\_representative\_samples passando esses dois conjuntos e definindo diversity\_per\_cluster=4, o que força o método a não escolher apenas um exemplo por grupo, mas sim um pequeno pacote por cluster que combina representatividade (chunks mais centrais) e diversidade (variações internas do mesmo tema), reduzindo a redun- dância e aumentando a cobertura do corpus sem aumentar o custo de leitura. Por fim, você encerra a execução com close(), fechando o conector e liberando recursos, mantendo o pipeline limpo para a próxima etapa.

**\#extrair tipos de entidades e relações sb \= SchemaBuilder()**

**schema \= sb.build\_schema(n\_entities=15, n\_relations=10, texts=sampled\_chunks)**

Para concluir, este bloco fecha a etapa de **detecção automá- tica**, transformando os chunks representativos em um vocabulá- rio controlado de **TIPOS**. Quando você instancia SchemaBuilder, você prepara um componente cuja função é ler os textos amos- trados (sampled\_chunks) e inferir, de forma agregada, quais pa- drões aparecem com mais frequência nesse subconjunto que repre- senta o corpus. Ao chamar build\_schema com n\_entities=15 e n\_relations=10, você está explicitando o orçamento do schema: peça para ele retornar apenas os 15 tipos de entidades mais co- muns e os 10 tipos de relacionamentos mais comuns observados nos chunks selecionados, reduzindo o ruído e evitando que o pi- peline exploda em variações redundantes.   O resultado disso é o schema em memória e, principalmente, a geração do arquivo **entities\_types.json**, que registra esses tipos mais recorrentes para você reutilizar como vocabulário fechado na extração em larga escala, garantindo consistência na criação de **nós** e **arestas** no Neo4j.

Com esses **tipos de entidades** e **tipos de relacionamentos** detectados e consolidados, o resto torna-se a execução disciplinada do que vocês já dominaram neste capítulo: peguem o vocabulário fechado do entities\_types.json, rodem a extração nos textos para produzir instâncias de entidades e arestas compatíveis com esse esquema, e então persistam tudo no Neo4j. A partir daí, você repete o pipeline completo sem inventar nada novo: valida no Brow- ser, projeta o grafo no GDS, calcula comunidades com Leiden, grava communityId e, por fim, gera e salva os resumos por comunidade para transformar o grafo em um índice consultável no GraphRAG. Ou seja, a detecção automática aqui apenas remove o gargalo ini- cial (definir TIPOS); uma vez que isso está resolvido, você aplica,

em escala, o mesmo processo de criação e exploração do grafo de conhecimento que já foi construído passo a passo neste capítulo.

**5.14 UM PROBLEMA SÉRIO COM GRAPHRAG**

Como eu sempre tenho o costume de falar "Na computação tudo é um perde e ganha". O GraphRAG ganha **estrutura** e **rastreabili- dade**, mas paga isso com um custo pesado de **tokens** justamente na etapa mais cara: detectar **entidades** e **relacionamentos** para mon- tar o grafo de conhecimento. Aqui não tem milagre: se o seu corpus vira milhares (ou milhões) de chunks, e você tenta extrair entidades e relações chamando uma LLM chunk a chunk, o número de cha- madas cresce quase linearmente com a quantidade de chunks, e a conta explode rápido porque cada chamada carrega instruções, con- texto, exemplos e ainda retorna um JSON estruturado. O resultado é simples: quanto maior a granularidade (chunks pequenos), maior a **cobertura**, mas maior também o volume de prompts e respostas, logo maior o consumo total de tokens para construir o grafo.

O impacto prático é que a etapa de **construção do grafo** vira o gargalo financeiro do pipeline: você não está só ’consultando’, você está **processando todo o corpus** para gerar nós e arestas, e isso significa pagar tokens para ler e rotular praticamente tudo. Se você ainda adicionar iterações (corrigir schema, refazer extração, reprocessar documentos novos, reindexar quando mudar o prompt), a conta não cresce por um fator, cresce por ciclos, porque você repete o mesmo trabalho em escala. Por isso, quando a quantidade

de chunks é alta, as chamadas à LLM crescem muito e o custo de tokens deixa de ser um detalhe e passa a ser uma restrição de projeto: ou você controla representatividade e reduz o que entra na LLM, ou você aceita que gerar o grafo completo por extração automática em larga escala é, por definição, uma operação cara.

**CAPÍTULO	6**  
O RAG Híbrido

Imagine um investigador analisando um caso complexo. Em alguns momentos, ele precisa folhear rapidamente pilhas de docu- mentos em busca de trechos que soem familiares. Em outros, precisa montar um quadro na parede, ligando fotos, nomes e eventos com fios para enxergar padrões que não aparecem em uma leitura direta. Se ele usar apenas um desses métodos, inevitavelmente perderá algo. O RAG híbrido nasce exatamente dessa dualidade entre busca rápida por semelhança e reconstrução explícita de relações.

No RAG baseado em vetores, a lógica se aproxima da leitura in- tensiva de documentos. O sistema recupera trechos semanticamente próximos à pergunta, o que funciona muito bem quando a resposta está explícita no texto. Porém, quando o conhecimento está diluído ao longo do corpus ou depende de múltiplas peças conectadas, essa leitura isolada começa a falhar.

Já no RAG baseado em grafos, o foco não está no texto em si, mas nas conexões extraídas dele. Entidades, relações e estruturas organizam o conhecimento de forma explícita. Isso permite raciocí- nios mais encadeados, mas também introduz limitações quando a pergunta é vaga, abstrata ou não referencia diretamente elementos do grafo.

O RAG híbrido surge como consequência natural desse cenário. Em vez de escolher um único ponto de vista, ele assume que diferen- tes formas de recuperação capturam diferentes aspectos do mesmo conhecimento. A recuperação deixa de ser monocromática e passa

a ser composta por múltiplas lentes operando em conjunto.

Esse movimento muda o papel do contexto no RAG. O contexto não é apenas algo parecido com a pergunta, nem apenas algo estruturalmente conectado. Ele passa a ser um artefato composto, onde a similaridade semântica e as relações explícitas coexistem e se reforçam. O resultado é um contexto mais rico e menos frágil frente a perguntas complexas.

**Link do projeto HybridRAG:**

[https://bit.ly/sandeco-hybridrag](https://bit.ly/sandeco-hybridrag)

**6.1 INDEXAÇÃO NO HYBRID RAG**

A indexação no HybridRAG deve ser tratadach como uma etapa **executada separadamente**, exatamente como foi ensinado ao longo do livro. No **Capítulo 2**, você aprendeu a indexar documentos e construir o RAG vetorial. Já no **Capítulo 5**, o foco foi criar o grafo de conhecimento, gerar comunidades e produzir os resumos das comunidades. O HybridRAG não reinventa esses processos; ele parte do pressuposto de que ambos já existem e estão corretamente construídos.

Aqui, o ponto central é compreender que o HybridRAG começa

**depois** que essas duas indexações estão prontas. Primeiro, o ín- dice vetorial completo. Segundo, o grafo de conhecimento com suas comunidades e resumos persistidos. Somente com essas duas me- mórias preparadas é que a recuperação híbrida faz sentido. Esta seção estabelece essa dependência explícita antes de avançarmos para como esses dois mundos passam a ser combinados no mo- mento da consulta. A Figura [6.1](#bookmark=id.unbjhxob43uj) mostra com se dá a indexação no HibridRAG.

Figura 6.1: Fluxo de indexação destacando a extração de entidades e relacionamentos como ponto de transição entre texto e grafo.

**6.2 A CONSULTA NO HYBRID RAG**

Entenda um ponto fundamental: a consulta no HybridRAG não é um mecanismo novo e isolado. Ela é a combinação explícita da con- sulta do RAG tradicional com a consulta do GraphRAG. Assim como a indexação dependeu de duas estruturas previamente construídas, a fase de recuperação também depende de dois caminhos paralelos que operam de forma coordenada.

Primeiro, execute a consulta vetorial exatamente como você apren- deu no **Capítulo 2**. Gere o embedding da pergunta, busque no índice vetorial e recupere os trechos semanticamente mais próximos. Esse é o braço de similaridade do sistema. Em paralelo, execute a con- sulta estrutural no grafo, como foi ensinado no **Capítulo 5**. Identifique entidades relevantes, navegue pelas relações, explore comunidades e, quando necessário, utilize os resumos comunitários já persistidos. Esse é o braço relacional do sistema.

Perceba que o HybridRAG não substitui nenhum dos dois. Ele orquestra ambos. A consulta deixa de ser linear e passa a ser composta: parte dela busca proximidade semântica; parte dela busca conexões explícitas. O contexto final não nasce de uma única fonte, mas da fusão controlada desses dois fluxos de recuperação.

Veja como os chunks são unidos na consulta, na Figura [6.2.](#bookmark=id.5o57kd9i8y9d) Observe que, ao receber a pergunta do usuário, você deve primeiro gerar o embedding da consulta e enviá-lo ao **Retriever**, que acessa o índice vetorial e retorna os trechos semanticamente mais próximos; em paralelo, acione o grafo e recupere os **Community Summaries**, permitindo que a estrutura relacional também contribua com contexto de alto nível. Em seguida, faça a etapa de **Merge chunks**: pegue os trechos vindos do vetor, combine com os resumos estruturais do grafo e construa um bloco único e coerente de informação. Não trate esses fluxos como concorrentes, trate-os como complementares; una similaridade semântica e conexão estrutural em um mesmo contexto enriquecido.  Depois disso, forme o bloco **Augmented**, garantindo

que todo o conteúdo consolidado esteja pronto para ser enviado à etapa de **Generation**. Perceba que a geração não nasce de uma única fonte, mas de um contexto já fundido, mais denso e menos frágil, e é exatamente essa fusão que caracteriza a consulta híbrida representada visualmente dentro da região verde.

Figura 6.2: Fluxo da consulta híbrida destacando a fusão entre recuperação vetorial e resumos estruturais antes da geração.

**Código Básico da Consulta**

Para reduzir o atrito na adoção de memória, implemente um fluxo mínimo no qual você instancia os componentes no início do script e executa a consulta do começo ao fim, como se estivesse validando a engrenagem inteira antes de evoluir a arquitetura; faça isso no arquivo ’memory.py’ para manter o ponto de entrada claro e fácil de testar.

Agora, leia o código em blocos coesos. Comece importando so- mente o que você vai usar e instanciando os objetos que orquestram a consulta. Entenda que você está separando responsabilidades: um componente consulta o grafo, outro monta o prompt, outro gera a resposta, e outro recupera chunks do índice vetorial. Faça essas instâncias uma única vez, no topo do script, para não recriar objetos a cada pergunta.

**import json**  
**from graph\_query.graph\_queries import GraphQuery from augmentation import Augmentation**

**from graphRAG.generation import Generation from retriever import Retriever**

**gq \= GraphQuery() augmentation \= Augmentation() generation \= Generation()**  
**retriever \= Retriever(collection\_name="docs")**

Em seguida, defina a consulta como uma string simples e direta. Escreva a pergunta exatamente como o usuário faria e use essa mesma variável ao longo do fluxo para manter consistência entre recuperação, augmentação e geração. Não misture múltiplas queries no mesmo script neste ponto; mantenha uma única query para você conseguir observar o comportamento do pipeline sem ruído.

**query \= "Quem foi Epiteto?"**

Depois, execute a recuperação vetorial pedindo um número con- trolado de resultados. Faça a chamada ao método de busca do retriever, ajuste n\_results para controlar a quantidade de chunks retornados e desligue o metadata quando você quer validar só o conteúdo textual retornado. Entenda que, aqui, você está montando a primeira metade do contexto que será entregue ao modelo.

**\#Buscar chunks VectorRAG**

**chunks \= retriever.search(query, n\_results=20, show\_metadata=False)**

Agora, complemente o contexto com os resumos vindos do grafo. Busque as comunidades que já possuem resumo e, em seguida, per- corra a lista para anexar cada summary ao mesmo array de chunks. Faça essa união de forma explícita para que, no final, você tenha uma única lista contendo tanto trechos recuperados por similaridade quanto resumos estruturais; repare que o acesso ao dicionário usa a chave ’summary’, então você deve garantir que a estrutura retornada por list\_communities\_with\_summary realmente tem esse campo.

**\#Buscar resumos do GraphRAG**  
**resumos \= gq.list\_communities\_with\_summary()**

**for resumo in resumos: chunks.append(resumo\[’summary’\])**

Por fim, gere o prompt com a query e o conjunto unificado de chunks, chame a geração e imprima a resposta. Faça a augmentação antes da geração para padronizar o formato do contexto entregue ao modelo, depois execute generation.generate com o prompt final, e feche imprimindo o resultado para inspecionar rapidamente a saída no terminal. Se algo vier vazio ou estranho, volte um passo e imprima chunks e resumos separadamente para conferir se o problema está na recuperação ou na montagem do prompt.

**prompt \= augmentation.generate\_prompt(query, chunks)**

**response \= generation.generate(prompt) print(response)**

Observe que, no projeto, existe um arquivo chamado ’view.py’ que encapsula exatamente esse fluxo de consulta em uma interface interativa construída com Streamlit; abra esse arquivo, verifique que ele instancia os mesmos componentes, captura a pergunta do usuá- rio via campo de entrada e executa a recuperação híbrida antes de

exibir a resposta na tela. Para executar a aplicação, vá até o diretório do projeto no terminal e rode o comando abaixo, garantindo que o ambiente virtual esteja ativo.

**streamlit run view.py**

Figura 6.3: Uma busca por assuntos globais

Figura 6.4: Uma busca por um determinado assunto (local)gemini

