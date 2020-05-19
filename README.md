# Generate Report Bib (GRB)

Este projeto é uma iniciativa do atual Representante Discente do Programa de Pós-graduação em Ciência da Computação (PPGCC/PUCRS) **[Olimar Teixeira Borges](https://github.com/olimarborges)**, que visa auxiliar na padronização das Referências Bibliográficas utilizadas nas Dissertações de Mestrado e Teses de Doutorado do PPGCC.

## Tabela de conteúdos

- [Utilização](#utilizacao)
- [Configuração ambiente Python](#configuracao)
  - [Ambiente virtual Python](#ambpython)
    - [Configurando o ambiente](#configamb)
- [Dependências do projeto](#dependencias)
- [Entendendo o GRB](#entendoGRB)
- [Utilizando o GRB](#utilizandoGRB)
  - [Possíveis situações de relatórios de erros](#possiveis-rel-erros)
    - [Erro no config.json](#erro-config)
    - [Erro no arquivo.bib](#erro-bib)
  - [Relatório com os avisos](#rel-avisos)
    - [Novo arquivo.bib](#novo-bib)
  - [Lembre-se](#lembre-se)
- [Agradecimentos](#agradecimentos)
- [Contribuindo](#contribuindo)

As verificações programadas neste projeto seguem a padronização definida no documento [Formatos de Monografias, Dissertações e Teses do PPGCC](http://www.pucrs.br/politecnica-prov/wp-content/uploads/sites/166/2018/10/padrao_teses_dissertacoes_monografias_PPGCC_18102018.pdf), como também o [Documento Auxiliar](https://github.com/ppgcc/DocumentosPPGCC) criado pelo mesmo representante.

## Utilização

Faça o download deste repositório (ou clone) em seu ambiente (computador). Lembre-se da pasta (local) aonde este projeto ficará.

## Configuração ambiente Python

Para que você possa executar este projeto, será necessário ter instalado em sua máquina o `Python3`. Se você já possui o ambiente configurado, pode pular este tópico.

### Ambiente virtual Python

Para quem ainda não tem instalado o Python3, sugiro fazer uso do `virtualenv`. É uma forma de criar ambientes virtuais para o uso do Python, com o objetivo de deixar as modificações e bibliotecas em um ambiente local e não global, não 'bagunçando' as configurações originais do seu ambiente Python, além de não deixar 'sujeira' de configurações e pacotes inatalados. Você pode configurar vários ambientes, de acordo com o que tiver desenvolvendo e assim, os pacotes instalados ficam específicos para cada ambiente.

#### Configurando o ambiente

Instale o Python3 seguindo os passos de acordo com o seu Sistema Operacional (SO):

- [Linux](https://python.org.br/instalacao-linux/)
- [MacOS](https://python.org.br/instalacao-mac/)
- [Windows](https://python.org.br/instalacao-windows/)

Com o Python3 devidamente instalado, abra o Terminal do seu SO e inicie o processo de criação do seu ambiente virtual. Primeiro instale o pacote para criar os ambientes virtuais:
```
pip install virtualenv
```

Em seguida, crie uma pasta para armazenar as suas máquinas virtuais (você pode fazer a criação da pasta pela interface gráfica do seu SO, se preferir):
```
C:\Users\user\Desktop> mkdir <virtualenv>
```
Substitua `<virtualenv>` pelo nome da pasta. Neste exemplo, a pasta será `virtualenv`. Lembre-se do caminho aonde você está com a linha de execução do ser Terminal (`C:\Users\user\Desktop`, por exemplo).

Crie um ambiente virtual para executar o Python:
```
C:\Users\user\Desktop> virtualenv virtualenv\virtual_1
```

Ative o ambiente virtual:
```
virtualenv\virtual_1\Scripts\activate
```

Agora, antes da linha de comando, aparecerá um flag (virtual_1) dizendo que você está usando o virtual env 'virtual_1':
```
(virtual_1) C:\Users\user\Desktop>
```
A partir daqui, você pode começar a instalar as bibliotecas que desejar. Para este projeto, vamos fazer uso do `pip` para instalar alguns pacotes.

## Dependências do projeto

Neste momento, acesse o local aonde o projeto foi baixado, por exemplo:

```
(virtual_1) C:\Users\user\Desktop> cd GenerateReportBib
(virtual_1) C:\Users\user\Desktop\GenerateReportBib>
```

Para que o projeto funcione, antes você precisa instalar alguns pocotes. Para facilitar este processo, execute o comando abaixo que ele importará todos os pacotes de uma só vez:

```
(virtual_1) C:\Users\user\Desktop\GenerateReportBib> pip install -r requirements.txt
```

## Entendendo o GRB

Se todos os passos anteriores foram executados sem problemas, você já pode fazer uso deste projeto.

Antes de iniciar o uso deste sistema, preste bastante atenção na estrutura de pastas do projeto. Ela é importante para que o funcionamento do script ocorra de maneira correta. Entenda a organização de pastas:

- *OriginalBIB:* É nesta pasta que você deve inserir o seu `arquivo.bib` original.
- *GenerateReports:* É nesta pasta que os relatórios com a lista de erros encontrados do seu `arquivo.bib` serão gerados. A cada nova execução do script, um novo relatório é gerado com a data e horário da geração.
- *GenerateBIB:* É nesta pasta que os novos arquivos .bib serão gerados. Após a execução do script, caso o seu bib não esteja com problemas de compilação, será gerado um `novo_arquivo.bib` aqui, com a mesma data e horário do relatório correspondente a mesma execução.
- *screenshots:* Pasta com as imagens de exemplo que constam neste arquivo `README.md`.

O arquivo principal `grb.py` é o script que realiza todo o processamento e verificações do seu `arquivo.bib`.

Para fazer uso do GRB você não precisa mexer no script. A sua edição só é estimulada, caso pretenda contribuir com melhorias e refatorações no código. Caso contrário, qualquer mudança pode ocasionar mal funcionamento na geração dos `relatórios de erros` e do `novo_arquivo.bib`.

Para iniciar efetivamente o uso do script, abra o arquivo `config.json`. Este arquivo serve como configuração de alguns parâmetros, para que o script funcione. Caso este arquivo não esteja devidamente configurado, o script gerará um relatório relatando a má configuração dos parâmetros e solicitando que sejam corrigidos para que seja possível dar continuidade na verificação. Corrija os parâmetros e execute o script novamente.

## Utilizando o GRB

Para fazer uso do script, inicialmente copie o seu `arquivo.bib` para dentro a pasta `OriginalBIB`. Em seguida, abra o arquivo de configuração `config.json`:
```
{
    "Comentários": [...	],
    "NAME-FILE" : "referencesTest",
    "LANGUAGE" : "english",
    "TYPE_REFERENCES" : "num-alpha"
}
```

Neste momento, preencha os parâmetros corretamente, seguindo as restrições de preencgimento especificadas no campo de "Comentários:"

- **NAME-FILE:** Preencha com o nome do seu `arquivo.bib` original (NÃO INFORME A EXTENSÃO) que precisa, obrigatoriamente, estar localizado na pasta `OriginalBIB`.",
- **LANGUAGE:** Idioma da sua Dissertação ou Tese. Para PORTUGUÊS utilize: `portuguese` / Para INGLÊS utilize: `english`)",
- **TYPE_REFERENCES:** Tipo das suas referências. Para estilos NUM ou ALPHA utilize: `num-alpha` / Para o estilo APALIKE utilize: `apa`"

Com os parâmetros devidamente configurados, você já pode fazer a execução do script. Para isso, abra o Terminal na linha de comando do seu projeto e execute:
```
(virtual_1) C:\Users\user\Desktop\GenerateReportBib>python grb.py
```

Se no console do seu Terminal aparecer a mensagem: `Exporting to arquivo.html`, significa que o script executou sem problemas. No entanto, isso não significa que o processo encerra aqui. O script gera mais de um tipo de relatório, portanto, para verificar quais foram os problemas encontrados, acesse a pasta `GenerateReports` e busque pelo arquivo `report.html`. O nome do relatório é gerado com a data e horário da execução do script, por exemplo: `_Report_2020-05-19_15-11-05.html`.

### Possíveis situações de relatórios de erros

Enquanto houverem problemas no `config.json` ou no seu `arquivo.bib`, serão gerados relatórios de erros e não gerá gerado o `novo_arquivo.bib`.

#### Erro no config.json

Caso os parâmetros do arquivo de configuração não tenham sido preenchidos de acordo, ou ainda, o nome do `arquivo.bib` especificado não se encontra na pasta `OriginalBIB`, a mensagem descrita no relatório explicará qual dos campos não está correto. Corrija e execute novamente o script.

#### Erro no arquivo.bib

Caso o seu `arquivo.bib` esteja com algum problema, o script ficará gerando relatórios de erros, até que o mesmo seja corrigido. Possíveis problemas no `arquivo.bib`, encontrados durante os testes, que geram problemas:

- Quando há labels de referências repetidos, como por exemplo:

```
@article{olimar2020,
  title={Título},
  author={Borges, Olimar Teixeira},
  journal={Journal},
  volume={30},
  pages={389-406},
  month={Mar},
  year={2020}
}

@inproceedings{olimar2020,
  title={Título},
  author={Borges, Olimar Teixeira},
  booktitle={Booktitle},
  pages={389-406},
  year={2020}
}
```

- Quando, em qualquer citação, haja a tag `month={}` preenchida com um mês 'não válido' OU vazio. Os meses precisam estar, obrigatoriamente, em inglês e abreviados até a terceira letra (podendo estar escitos em minúsculo ou maiúsculo). Mesmo que a sua Dissertação ou Tese esteja em português.
  * `Esta é uma restrição do pacote` **_pybtex_** `utilizado neste projeto. Infelizmente, não foi possível corrigir esta questão até o momento.`

- Os labels programados para funcionarem neste script são: _`@book, @article, @inproceedings @proceedings, @mastersthesis, @phdthesis, @techreport, @misc, @booklet, @inbook, incollection`_. Qualquer outro label de referência que estiver dentro do `arquivo.bib`, gerará um relatório de erro.

Veja um exemplo de relatório que não gera o `novo_arquivo.bib`, devido aos erros mencionados anteriormente:

![](screenshots/reportErrorOriginalBIB.PNG)

### Relatório com os avisos

Este relatório é o principal deste projeto! Ele é gerado quando não há erros nos arquivos `config.json` e `arquivo.bib`.

Neste relatório é apresentado as validações que o script realizou. Para cada uma das referências do `arquivo.bib`, que for identificado alguma inconsistência, será listada a referência e o aviso que deve ser verificado. No coluna `Warning` consta as descrições que devem ser corrigidas. Veja o screenshot de exemplo de um relatório de avisos final:

![](screenshots/reportWarning.PNG)

#### Novo arquivo.bib

Junto com este relatório dos avisos, é gerado um `novo_arquivo.bib`. Neste arquivo, para as referências que possuírem `campos faltantes`, será inserido neste novo arquivo a tag faltante e o valor `MISSING`, para que seja possível buscar rapidamente por esta palavra e fazer a adequação (inserir a informação que falta).

Por exemplo, caso no `arquivo.bib` conste a seguinte referência, com a configuração `english` e `num-alpha`:

```
@book{LabelDaCitacao,
	title={Computers as components: principles of embedded computing system design},
	author={W. Wolf},
	year={2001},
	address={New York, EUA}
}
```

No arquivo de relatório será apresentada para esta referênicia a mensagem: `Missing: {'publisher', 'numpages'}`. Já que os campos obrigatórios para livros no estilo `num-alpha` são: `{'author', 'title', 'publisher', 'year', 'numpages'}`. E além desta informação, será gerado no `novo_arquivo.bib` a seguinte referência:

```
@book{LabelDaCitacao,
	title={Computers as components: principles of embedded computing system design},
	author={W. Wolf},
	year={2001},
	address={New York, EUA},
  publisher={MISSING},
  numpages={MISSING}
}
```

Para cada referência com campos faltantes, será gerada uma correspondente neste novo arquivo, com a `tag={MISSING}`.

### LEMBRE-SE!

**Devido à restrição mencionada anteriormente do pacote `pybtex`, as informações dos meses precisam estar dentro das definições da biblioteca. Neste caso, se você estiver escrevendo seu volume em português e precise fazer a adequação dos meses (colocá-los em inglês) no seu `arquivo.bib` para que executar este script, lembre-se de voltar os meses para o português na versão final.**


## Agradecimentos
Agradecimento ao ex-colega e amigo [Pedro Ballester](https://github.com/Ballester) pela disponibilização do código embrião deste projeto!

## Contribuindo
Se você acha este projeto útil e gostaria de contribuir com ele, fique à vontade em fazer alterações e refatorações no código e em seguida abra [pull requests](https://help.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) para se tornarem parte oficial deste projeto.
