using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SqlClient;
using System.Diagnostics;

namespace Project
{
    public partial class AddEstabelec : Form
    {
        private SqlConnection CN = new SqlConnection();

        public AddEstabelec()
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

        private void AddEstbelec_Load(object sender, EventArgs e)
        {
            String[] hours = { "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"
                                , "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "12:30", "13:00"
                                , "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00"
                                , "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"};

            for (int i = 0; i < AppData.stablish.Length; i++) {
                comboBox3.Items.Add(AppData.stablish[i]);
            }
            for (int i = 0; i < hours.Length; i++) {
                comboBox1.Items.Add(hours[i]);
                comboBox2.Items.Add(hours[i]);
            }

            comboBox1.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
            comboBox3.SelectedIndex = 0;
        }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {
            String text = ((sender as System.Windows.Forms.ComboBox).SelectedItem).ToString();
            updateFunc(text);
        }

        private void updateFunc(String estabelec)
        {
            comboBox4.Items.Clear();
            if (estabelec == "Piscina") {
                label5.Text = "Temperatura da Água";
                textBox2.Text = "";
                textBox2.Visible = true;
                comboBox4.Visible = false;
            } else if (estabelec == "Ginásio") {
                label5.Text = "Número de Aparelhos";
                textBox2.Text = "";
                textBox2.Visible = true;
                comboBox4.Visible = false;
            } else if (estabelec == "Pista") {
                label5.Text = "Tipo de Solo";
                for (int i = 0; i < AppData.soil.Length; i++) {
                    comboBox4.Items.Add(AppData.soil[i]);
                }

                textBox2.Visible = false;
                comboBox4.Visible = true;
                comboBox4.SelectedIndex = 0;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String open = comboBox1.SelectedItem.ToString();
            String close = comboBox2.SelectedItem.ToString();
            String maintenance = monthCalendar1.SelectionStart.ToString("yyyy-MM-dd");
            String capacity = textBox1.Text;
            String type = comboBox3.SelectedItem.ToString();
            
            try {
                int n = Int32.Parse(capacity);

                try {
                    CN = getSGBDConnection();
                    if (!verifySGBDConnection())
                    {
                        MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                        return;
                    }

                    SqlCommand cmd = new SqlCommand();
                    cmd.Connection = CN;
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.Add("@hora_aberto", SqlDbType.Time).Value = open;
                    cmd.Parameters.Add("@hora_fechado", SqlDbType.Time).Value = close;
                    cmd.Parameters.Add("@data_manutencao", SqlDbType.Date).Value = maintenance;
                    cmd.Parameters.Add("@lotacao", SqlDbType.Float).Value = capacity;

                    if (type == "Piscina") {
                        try {
                            var temp = float.Parse(textBox2.Text);
                            cmd.Parameters.Add("@temp_agua", SqlDbType.Int).Value = temp;
                            cmd.CommandText = "sp_add_piscina";
                        } catch (Exception ex) {
                            MessageBox.Show("Temperatura de Água Inválida!");
                            return;
                        }
                    }

                    if (type == "Ginásio") {
                        try {
                            var aparelhos = Int32.Parse(textBox2.Text);
                            cmd.Parameters.Add("@qtd_aparelhos", SqlDbType.Int).Value = aparelhos;
                            cmd.CommandText = "sp_add_ginasio";
                        } catch (Exception ex) {
                            MessageBox.Show("Número de Aparelhos Inválido!");
                            return;
                        }
                    }

                    if (type == "Pista") {
                        var solo = comboBox4.SelectedItem.ToString();
                        cmd.Parameters.Add("@tipo_solo", SqlDbType.VarChar).Value = solo;
                        cmd.CommandText = "sp_add_pista";
                    }

                    int result = cmd.ExecuteNonQuery();
                    Debug.Print(result.ToString());

                    MessageBox.Show("Estabelecimento adicionado com sucesso!");
                    this.Hide();

                    CN.Close();
                } catch(Exception ex) {
                    MessageBox.Show(ex.Message);
                    MessageBox.Show("Dados introduzido inválidos");
                }
            }
            catch (Exception ex) {
                MessageBox.Show("Lotação Inválida!");
            }
        }
    }
}
