using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Forms;
using System.Data.SqlClient;
using System.Diagnostics;

namespace Project
{
    public partial class Reserva : Form
    {
        public String[] meses = { "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro" };
        private SqlConnection CN = new SqlConnection();
        public String start_hour = "";
        public String duration = "";

        public Reserva()
        {
            InitializeComponent();

            String[] hours = { "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"
                                , "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "12:30", "13:00"
                                , "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00"
                                , "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"};
            for (int i = 0; i < hours.Length; i++) {
                 comboBox1.Items.Add(hours[i]);
            }

            String[] duration = { "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00" };
            for (int i = 0; i < duration.Length; i++) {
                comboBox2.Items.Add(duration[i]);
            }
            
            comboBox1.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
        }
        private SqlConnection getSGBDConnection()
        {
            return new SqlConnection("Data Source = " + AppData.DB_STRING + " ;" + "Initial Catalog = " + AppData.username + "; uid = " + AppData.username + ";" + "password = " + AppData.password);
        }

        private bool verifySGBDConnection()
        {
            if (CN == null)
                CN = getSGBDConnection();

            if (CN.State != ConnectionState.Open)
                CN.Open();

            return CN.State == ConnectionState.Open;
        }

        private void Reserva_Load(object sender, EventArgs e)
        {
            String date = ReservaData.picked_date;
            String[] date_info = date.Split('-');
            label1.Text = "Reserva para dia " + date_info[2] + " de " + meses[Int32.Parse(date_info[1])-1] + " de " + date_info[0];
            label2.Text = "Número de Inscrição: " + ReservaData.num_insc;
        }

        private void loadTable() {
            comboBox3.Items.Clear();
            comboBox4.Items.Clear();

            CN = getSGBDConnection();
            if (!verifySGBDConnection())
                return;

            if (start_hour != "" && duration != "") {
                Debug.Print("SELECT * FROM Reserva_disponivel(\'" + ReservaData.picked_date + "\',\'" + start_hour + "\',"
                    + "DATEADD(minute, (DATEDIFF(MINUTE, 0, \'" + duration + "\')), \'" + start_hour + "\')," + ReservaData.num_insc + ")");
                SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM Reserva_disponivel(\'" + ReservaData.picked_date + "\',\'" + start_hour + "\'," 
                    + "DATEADD(minute, (DATEDIFF(MINUTE, 0, \'" + duration + "\')), \'" + start_hour + "\')," + ReservaData.num_insc + ")"
                    , CN);
                DataTable dt = new DataTable();
                sqldata.Fill(dt);

                dataGridView1.DataSource = dt;

                SqlCommand cmd = new SqlCommand("SELECT * FROM Reserva_disponivel(\'" + ReservaData.picked_date + "\',\'" + start_hour + "\',"
                    + "DATEADD(minute, (DATEDIFF(MINUTE, 0, \'" + duration + "\')), \'" + start_hour + "\')," + ReservaData.num_insc + ")"
                    , CN);
                
                SqlDataReader reader = cmd.ExecuteReader();
                
                while(reader.Read()) {
                    if (!comboBox3.Items.Contains("Estabelecimento " + reader[0].ToString()))
                        comboBox3.Items.Add("Estabelecimento " + reader[0].ToString());
                    if (!comboBox4.Items.Contains(reader[2].ToString() + " (id: " + reader[1].ToString() + ")"))
                        comboBox4.Items.Add(reader[2].ToString() + " (id: " + reader[1].ToString() + ")");
                }
                
                CN.Close();
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            start_hour = comboBox1.SelectedItem.ToString();
            loadTable();
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            duration = comboBox2.SelectedItem.ToString();
            loadTable();
        }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            String estabelecimento = comboBox3.SelectedItem == null ? "" : comboBox3.SelectedItem.ToString();
            String treinador = comboBox4.SelectedItem == null ? "aa" : comboBox4.SelectedItem.ToString();

            if (estabelecimento != "" && treinador != "") {
                estabelecimento = estabelecimento.Substring(16);
                treinador = treinador.Split(new[] { " (id: " }, StringSplitOptions.None)[1];
                treinador = treinador.Substring(0, treinador.Length - 1);

                Debug.Print(estabelecimento);
                Debug.Print(treinador);

                CN = getSGBDConnection();
                if (!verifySGBDConnection())
                    return;
                
                try {
                    SqlCommand cmd = new SqlCommand("INSERT INTO Reserva VALUES (" + treinador + "," + ReservaData.num_insc + ",\'" + ReservaData.picked_date
                        + "\',\'" + start_hour + "\',\'" + duration + "\'," + estabelecimento + ")", CN);

                    Debug.Print("INSERT INTO Reserva VALUES(" + treinador + ", " + ReservaData.num_insc + ",\'" + ReservaData.picked_date
                        + "\',\'" + start_hour + "\',\'" + duration + "\'," + estabelecimento + ")");

                    cmd.ExecuteNonQuery();

                    MessageBox.Show("Reserva adicionada com sucesso!");
                    this.Hide();
                } catch(Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } else{
                MessageBox.Show("Dados introduzidos inváldos!");
            }
        }
    }
}
