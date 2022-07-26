using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project
{
    class AppData
    {
        public static String DB_STRING = "tcp:mednat.ieeta.pt\\SQLSERVER,8101";
        public static String username = "p2g1";
        public static String password = "Zuquet3!";
        public static String[] sports = { "Judo", "Ténis", "Basquetebol", "Atletismo", "Voleibol", "Badminton", "Rugby", "Natacão" };
        public static String[] funcs = { "Treinador", "Empregado de Saúde", "Secretariado" };
        public static String[] health = { "Fisioterapia", "Medicina Geral", "Nutricão", "Oftalmologia", "Cardiologia" };
        public static String[] stablish = { "Piscina", "Ginásio", "Pista" };
        public static String[] soil = { "Esteira", "Argila", "Areia", "Sintética", "Asfalto", "Relva" };
    }
}
