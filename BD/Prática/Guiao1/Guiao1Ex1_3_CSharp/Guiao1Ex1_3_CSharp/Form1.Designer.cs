
namespace Guiao1Ex1_3_CSharp
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.l2 = new System.Windows.Forms.Label();
            this.l3 = new System.Windows.Forms.Label();
            this.l1 = new System.Windows.Forms.Label();
            this.server = new System.Windows.Forms.TextBox();
            this.user = new System.Windows.Forms.TextBox();
            this.pass = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // l2
            // 
            this.l2.AutoSize = true;
            this.l2.Location = new System.Drawing.Point(28, 90);
            this.l2.Name = "l2";
            this.l2.Size = new System.Drawing.Size(29, 13);
            this.l2.TabIndex = 0;
            this.l2.Text = "User";
            this.l2.Click += new System.EventHandler(this.label1_Click);
            // 
            // l3
            // 
            this.l3.AutoSize = true;
            this.l3.Location = new System.Drawing.Point(28, 147);
            this.l3.Name = "l3";
            this.l3.Size = new System.Drawing.Size(53, 13);
            this.l3.TabIndex = 1;
            this.l3.Text = "Password";
            this.l3.Click += new System.EventHandler(this.label2_Click);
            // 
            // l1
            // 
            this.l1.AutoSize = true;
            this.l1.Location = new System.Drawing.Point(28, 40);
            this.l1.Name = "l1";
            this.l1.Size = new System.Drawing.Size(38, 13);
            this.l1.TabIndex = 2;
            this.l1.Text = "Server";
            // 
            // server
            // 
            this.server.Location = new System.Drawing.Point(105, 37);
            this.server.Name = "server";
            this.server.Size = new System.Drawing.Size(298, 20);
            this.server.TabIndex = 3;
            // 
            // user
            // 
            this.user.Location = new System.Drawing.Point(105, 87);
            this.user.Name = "user";
            this.user.Size = new System.Drawing.Size(298, 20);
            this.user.TabIndex = 4;
            // 
            // pass
            // 
            this.pass.Location = new System.Drawing.Point(105, 140);
            this.pass.Name = "pass";
            this.pass.Size = new System.Drawing.Size(298, 20);
            this.pass.TabIndex = 5;
            this.pass.UseSystemPasswordChar = true;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(105, 189);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(136, 74);
            this.button1.TabIndex = 6;
            this.button1.Text = "Test Ligação";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(274, 189);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(129, 74);
            this.button2.TabIndex = 7;
            this.button2.Text = "Hello Table";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(444, 275);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.pass);
            this.Controls.Add(this.user);
            this.Controls.Add(this.server);
            this.Controls.Add(this.l1);
            this.Controls.Add(this.l3);
            this.Controls.Add(this.l2);
            this.Name = "Form1";
            this.Text = "Aula 1 BD";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label l2;
        private System.Windows.Forms.Label l3;
        private System.Windows.Forms.Label l1;
        private System.Windows.Forms.TextBox server;
        private System.Windows.Forms.TextBox user;
        private System.Windows.Forms.TextBox pass;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
    }
}

