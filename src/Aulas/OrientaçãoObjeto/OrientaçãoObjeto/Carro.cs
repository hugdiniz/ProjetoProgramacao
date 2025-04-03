using System;
using System.Collections.Generic;
using System.Text;

namespace OrientaçãoObjeto
{
    class Carro
    {
        public String cor;
        public int ano;
        public Carro(string corEntrada,int anoCarro)
        {
            cor = corEntrada;
            ano = anoCarro;
        }

        public Boolean pagaIpva()
        {
            if(ano < 2010)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    }
}
