using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Data.SqlClient;

namespace Project
{
    public partial class Main : Form
    {
        public bool deleteEstabelecimento = false;
        public bool deleteFunc = false;
        public bool deleteAtleta = false;
        private SqlConnection CN = new SqlConnection();

        public Main()
        {
            InitializeComponent();
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

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            ReservaData form = new ReservaData();
            form.Show();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            AddAtleta form = new AddAtleta();
            form.Show();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            AddFunc form = new AddFunc();
            form.Show();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            AddEstabelec form = new AddEstabelec();
            form.Show();
        }

        private void tabPage4_Click(object sender, EventArgs e)
        {
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (deleteEstabelecimento == false) {
                deleteEstabelecimento = true;

                textBox1.Visible = true;
                label1.Visible = true;
                button8.Visible = true;
            } else {
                deleteEstabelecimento = false;

                textBox1.Visible = false;
                label1.Visible = false;
                button8.Visible = false;
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            if (deleteFunc == false) {
                deleteFunc = true;

                textBox2.Visible = true;
                label2.Visible = true;
                button9.Visible = true;
            } else {
                deleteFunc = false;

                textBox2.Visible = false;
                label2.Visible = false;
                button9.Visible = false;
            }
        }

        private void button7_Click(object sender, EventArgs e)
        {
            if (deleteAtleta == false) {
                deleteAtleta = true;

                textBox3.Visible = true;
                label3.Visible = true;
                button10.Visible = true;
            } else {
                deleteAtleta = false;

                textBox3.Visible = false;
                label3.Visible = false;
                button10.Visible = false;
            }
        }

        private void button8_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                SqlCommand cmd = new SqlCommand("DELETE FROM Estabelecimento WHERE id=" + textBox1.Text, CN);
                int result = cmd.ExecuteNonQuery();

                if (result == 0) {
                    textBox1.Text = "";
                    MessageBox.Show("Estabelecimento não existe");
                } else {
                    textBox1.Text = "";
                    MessageBox.Show("Estabelecimento removido com sucesso!");
                    CN.Close();
                }
            } catch(Exception ex) {
                MessageBox.Show("Estabelecimento inválido");
            }
        }

        private void button9_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                SqlCommand cmd = new SqlCommand("DELETE FROM Empregado WHERE n_func=" + textBox2.Text, CN);
                int result = cmd.ExecuteNonQuery();

                if (result == 0) {
                    textBox2.Text = "";
                    MessageBox.Show("Empregado não existe");
                } else {
                    textBox2.Text = "";
                    MessageBox.Show("Empregado removido com sucesso!");
                    CN.Close();
                }
            } catch (Exception ex) {
                MessageBox.Show("Empregado inválido");
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                Debug.Print("DELETE FROM Atleta WHERE n_inscricao=" + textBox3.Text);
                SqlCommand cmd = new SqlCommand("DELETE FROM Atleta WHERE n_inscricao=" + textBox3.Text, CN);
                int result = cmd.ExecuteNonQuery();

                if (result == 0) {
                    textBox3.Text = "";
                    MessageBox.Show("Atleta não existe");
                } else {
                    textBox3.Text = "";
                    MessageBox.Show("Atleta removido com sucesso!");
                    CN.Close();
                }
            } catch (Exception ex) {
                MessageBox.Show("Atleta inválido");
            }
        }

        private void button12_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_func = Int32.Parse(textBox4.Text);

                try {
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM Reserva WHERE n_func_treinador=" + n_func, CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView1.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } catch(Exception ex) {
                textBox4.Text = "";
                MessageBox.Show("Número de Funcionário Inválido");
            }
        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void button16_Click(object sender, EventArgs e)
        {
            label7.Text = "Reservas";
            dataGridView2.Visible = true;
            dataGridView3.Visible = false;
            dataGridView4.Visible = false;

            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_insc = Int32.Parse(textBox5.Text);

                try {
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM Reserva WHERE n_insc_atleta=" + n_insc, CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView2.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } catch (Exception ex) {
                textBox5.Text = "";
                MessageBox.Show("Número de Atleta Inválido");
            }
        }

        private void button11_Click(object sender, EventArgs e)
        {
            label7.Text = "Estatisticas Pessoais";
            dataGridView2.Visible = false;
            dataGridView3.Visible = true;
            dataGridView4.Visible = false;

            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_insc = Int32.Parse(textBox5.Text);

                try {
                    Debug.Print("SELECT st.num_reserva, avaliacao, data_reserva FROM Sessao_Treino st INNER JOIN Reserva r ON r.num_reserva = st.num_reserva WHERE r.n_insc_atleta=" + n_insc);
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT st.num_reserva, avaliacao, data_reserva FROM Sessao_Treino st INNER JOIN Reserva r ON r.num_reserva = st.num_reserva WHERE r.n_insc_atleta=" + n_insc, CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView3.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } catch (Exception ex) {
                textBox5.Text = "";
                MessageBox.Show("Número de Atleta Inválido");
            }
        }

        private void button17_Click(object sender, EventArgs e)
        {
            label7.Text = "Estatisticas Gerais";
            dataGridView2.Visible = false;
            dataGridView3.Visible = false;
            dataGridView4.Visible = true;

            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_insc = Int32.Parse(textBox5.Text);

                try{
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM melhores_avaliacoes_por_modalidade", CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView4.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } catch (Exception ex) {
                textBox5.Text = "";
                MessageBox.Show("Número de Atleta Inválido");
            }
        }

        private void button13_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int reserva = Int32.Parse(textBox8.Text);
                try {
                    int avaliacao = Int32.Parse(textBox7.Text);
                    Debug.Print("INSERT INTO Sessao_Treino VALUES(" + reserva + ", " + avaliacao + ")");

                    SqlCommand cmd = new SqlCommand("INSERT INTO Sessao_Treino VALUES(" + reserva + "," + avaliacao + ")", CN);
                    cmd.ExecuteNonQuery();

                    MessageBox.Show("Sessao registada com sucesso!");
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                    MessageBox.Show("Avaliação Inválida!");
                }
            } catch (Exception ex) {
                MessageBox.Show("Número de reserva inválido!");
            }
        }

        private void label8_Click(object sender, EventArgs e)
        {

        }

        private void textBox8_TextChanged(object sender, EventArgs e)
        {

        }

        private void button18_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_func = Int32.Parse(textBox6.Text);

                try {
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM Consulta WHERE n_func_emp=" + n_func, CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView5.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            }
            catch (Exception ex)
            {
                textBox6.Text = "";
                MessageBox.Show("Número de Funcionário Inválido");
            }
        }

        private void button15_Click(object sender, EventArgs e)
        {
            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                int n_insc = Int32.Parse(textBox9.Text);

                try {
                    SqlDataAdapter sqldata = new SqlDataAdapter("SELECT * FROM Consulta WHERE n_insc_atleta=" + n_insc, CN);
                    DataTable dt = new DataTable();
                    sqldata.Fill(dt);

                    dataGridView5.DataSource = dt;
                } catch (Exception ex) {
                    MessageBox.Show(ex.Message);
                }
            } catch (Exception ex) {
                textBox9.Text = "";
                MessageBox.Show("Número de Atleta Inválido");
            }
        }

        private void button14_Click(object sender, EventArgs e)
        {
            Consulta form = new Consulta();
            form.Show();
        }
    }
}
