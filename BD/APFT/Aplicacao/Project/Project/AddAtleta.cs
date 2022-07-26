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
    public partial class AddAtleta : Form
    {
        private SqlConnection CN = new SqlConnection();

        public AddAtleta()
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

        private void AddAtleta_Load(object sender, EventArgs e)
        {
            for (int i = 0; i < AppData.sports.Length; i++) {
                comboBox1.Items.Add(AppData.sports[i]);
            }
            comboBox1.SelectedIndex = 0;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String date = monthCalendar1.SelectionStart.ToString("yyyy-MM-dd");
            String name = textBox1.Text;
            String sport = comboBox1.SelectedItem.ToString();

            CN = getSGBDConnection();
            if (!verifySGBDConnection())
            {
                MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                return;
            }

            try {
                if (name == "") {
                    MessageBox.Show("Nome Inválido");
                } else {
                    SqlCommand cmd = new SqlCommand("INSERT INTO Atleta VALUES(\'" + name + "\',\'" + date + "\',\'" + sport + "\',DEFAULT)", CN);
                    cmd.ExecuteNonQuery();
                    MessageBox.Show("Atleta adicionada com sucesso!");
                    this.Hide();
                }
            } catch(Exception ex) {
                MessageBox.Show("Atleta tem que ter 14 anos");
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void monthCalendar1_DateChanged(object sender, DateRangeEventArgs e)
        {

        }
    }
}
