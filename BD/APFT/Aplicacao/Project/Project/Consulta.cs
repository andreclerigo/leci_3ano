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
    public partial class Consulta : Form
    {
        private SqlConnection CN = new SqlConnection();

        public Consulta()
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

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void Consulta_Load(object sender, EventArgs e)
        {
            comboBox1.Items.Clear();
            comboBox1.Items.Add("Apto");
            comboBox1.Items.Add("Inapto");
            comboBox1.SelectedIndex = 0;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try {
                int n_func = Int32.Parse(textBox1.Text);

                try {
                    int n_insc = Int32.Parse(textBox2.Text);
                    String date = monthCalendar1.SelectionStart.ToString("yyyy-MM-dd");
                    String state = comboBox1.SelectedItem.ToString();

                    try {
                        CN = getSGBDConnection();
                        if (!verifySGBDConnection())
                        {
                            MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                            return;
                        }

                        SqlCommand cmd = new SqlCommand("INSERT INTO Consulta VALUES(" + n_func + "," + n_insc + ",\'" + date + "\',\'" + state + "\')", CN);
                        cmd.ExecuteNonQuery();

                        MessageBox.Show("Consulta registada com sucesso!");
                        this.Hide();
                    }
                    catch (Exception ex) {
                        MessageBox.Show(ex.Message);
                        MessageBox.Show("Dados introduzido Inválido!");
                    }
                } catch(Exception ex) {
                    MessageBox.Show("Número de Inscrição do Atleta é Inválido");
                }
            } catch(Exception ex) {
                MessageBox.Show("Número de Funcionário Inválido");
            }
        }
    }
}
