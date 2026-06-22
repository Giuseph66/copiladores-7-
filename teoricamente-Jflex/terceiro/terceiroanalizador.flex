%%

%standalone

Letra = [a-zA-Z]
Digito = [0-9]
Palavra = {Letra}*
Numero = {Digito}+

%%

{Numero} {System.out.println("> Encontrei um {numero}");}

{Palavra} {System.out.println("> Encontrei uma {palavra}");}
