using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Windows.Forms;
using System.Diagnostics;
using System.Data.SqlClient;

namespace Project
{
    public partial class ReservaData : Form
    {
        public static String picked_date = "";
        public static int num_insc = 0;
        private SqlConnection CN = new SqlConnection();

        public ReservaData()
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

        private void ResevaData_Load(object sender, EventArgs e)
        {
            
        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            try {
                num_insc = Int32.Parse(textBox1.Text);

                CN = getSGBDConnection();
                if (!verifySGBDConnection()) {
                    MessageBox.Show("FAILED TO OPEN CONNECTION TO DATABASE", "Connection Test", MessageBoxButtons.OK);
                    return;
                }

                SqlCommand cmd = new SqlCommand("SELECT * FROM Atleta WHERE n_inscricao=" + num_insc, CN);
                SqlDataReader reader = cmd.ExecuteReader();

                if (reader.HasRows) {
                    if (DateTime.Now.Date.CompareTo(monthCalendar1.SelectionStart.Date) > 0) {
                        throw new Exception("Data Inválida!");
                    } else {
                        this.Hide();
                        Reserva form = new Reserva();
                        form.Show();

                        CN.Close();
                        reader.Close();
                    }
                } else {
                    throw new Exception("Atleta não existe!");
                }
            } catch (Exception ex) {
                if (ex.Message == "Atleta não existe!") {
                    MessageBox.Show(ex.Message);
                } else if (ex.Message == "Data Inválida!") {
                    MessageBox.Show(ex.Message);
                } else {
                    textBox1.Text = "";
                    MessageBox.Show("Número de Inscrição inválido");
                }
            }
        }

        private void monthCalendar1_DateChanged(object sender, DateRangeEventArgs e)
        {
            picked_date = monthCalendar1.SelectionStart.ToString("yyyy-MM-dd");
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
