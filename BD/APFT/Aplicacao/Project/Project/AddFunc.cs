using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Controls;
using System.Data.SqlClient;
using System.Diagnostics;

namespace Project
{
    public partial class AddFunc : Form
    {
        private SqlConnection CN = new SqlConnection();

        public AddFunc()
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

        private void AddFunc_Load(object sender, EventArgs e)
        {
            for (int i = 0; i < AppData.funcs.Length; i++)
            {
                comboBox1.Items.Add(AppData.funcs[i]);
            }
            comboBox1.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
        }


        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            String text = ((sender as System.Windows.Forms.ComboBox).SelectedItem).ToString();
            updateFunc(text);
        }

        private void updateFunc(String func)
        {
            comboBox2.Items.Clear();
            if (func == "Treinador") {
                label5.Text = "Modalidade";
                for (int i = 0; i < AppData.sports.Length; i++) {
                    comboBox2.Items.Add(AppData.sports[i]);
                }
                comboBox2.SelectedIndex = 0;
            } else if (func == "Empregado de Saúde") {
                label5.Text = "Especialidade";
                for (int i = 0; i < AppData.health.Length; i++) {
                    comboBox2.Items.Add(AppData.health[i]);
                }
                comboBox2.SelectedIndex = 0;
            } else if (func == "Secretariado") {
                label5.Text = "Establecimento";
                
                CN = getSGBDConnection();
                if (!verifySGBDConnection())
                {
                    MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                    return;
                }

                SqlCommand cmd = new SqlCommand("SELECT * FROM Estabelecimento", CN);
                SqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read()) {
                    comboBox2.Items.Add("Estabelecimento " + reader["id"].ToString());
                }
                comboBox2.SelectedIndex = 0;

                CN.Close();
                reader.Close();
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (textBox1.Text == "") {
                MessageBox.Show("Nome Inválido!");
            } else {
                try {
                    float salario = float.Parse(textBox2.Text);
                    try {
                        int nif = Int32.Parse(textBox3.Text);

                        if (textBox3.Text.Length != 9) {
                            MessageBox.Show("NIF Inválido");
                        } else {
                            try {
                                String func = (comboBox1.SelectedItem).ToString();

                                CN = getSGBDConnection();
                                if (!verifySGBDConnection())
                                {
                                    MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                                    return;
                                }

                                SqlCommand cmd = new SqlCommand();
                                cmd.Connection = CN;
                                cmd.CommandType = CommandType.StoredProcedure;
                                cmd.Parameters.Add("@nome", SqlDbType.VarChar).Value = textBox1.Text;
                                cmd.Parameters.Add("@salario", SqlDbType.Float).Value = salario;
                                cmd.Parameters.Add("@nif", SqlDbType.Int).Value = nif;

                                if (func == "Treinador") {
                                    cmd.Parameters.Add("@modalidade", SqlDbType.VarChar).Value = (comboBox2.SelectedItem).ToString();
                                    cmd.CommandText = "sp_add_treinador";
                                }

                                if (func == "Empregado de Saúde") {
                                    cmd.Parameters.Add("@especialidade", SqlDbType.VarChar).Value = (comboBox2.SelectedItem).ToString();
                                    cmd.CommandText = "sp_add_emp_saude";
                                }

                                if (func == "Secretariado") {
                                    cmd.Parameters.Add("@id_estabelecimento", SqlDbType.Int).Value = Int32.Parse((comboBox2.SelectedItem).ToString().Substring(16));
                                    cmd.CommandText = "sp_add_secretariado";
                                }

                                int result = cmd.ExecuteNonQuery();

                                MessageBox.Show("Funcionário adicionado com sucesso!");
                                this.Hide();

                                CN.Close();
                            } catch (Exception ex) {
                                MessageBox.Show("Dados Inválidos");
                            }
                        }
                    } catch (Exception ex) {
                        MessageBox.Show("NIF Inválido");
                    }
                } catch(Exception ex) {
                    MessageBox.Show("Salário Inválido!");
                }
            }
        }
    }
}
