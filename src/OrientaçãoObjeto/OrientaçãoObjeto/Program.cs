using System;

namespace OrientaçãoObjeto
{
    class Program
    {
        static void Main(string[] args)
        {
            Carro c = new Carro("preto",2009);

            Console.WriteLine(c.pagaIpva());
        }
    }
}
