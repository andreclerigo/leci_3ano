﻿Imports System.Data.SqlClient

Public Class Form1
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Label1_Click(sender As Object, e As EventArgs) Handles Label1.Click

    End Sub

    Private Sub Label3_Click(sender As Object, e As EventArgs) Handles Label3.Click

    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        TestDBConnection(server.Text, "", user.Text, pass.Text)
    End Sub

    Private Sub TestDBConnection(ByVal dbServer As String, ByVal dbName As String, ByVal userName As String, ByVal userPass As String)

        Dim CN As New SqlConnection("Data Source = " + dbServer + " ;" + "Initial Catalog = " + dbName + "; uid = " + userName + ";" + "password = " + userPass)

        Try
            CN.Open()
            If CN.State = ConnectionState.Open Then
                MsgBox("Successful connection to database " + CN.Database + " on the " + CN.DataSource + " server", MsgBoxStyle.OkOnly, "Connection Test")
            End If

        Catch ex As Exception
            MsgBox("FAILED TO OPEN CONNECTION TO DATABASE DUE TO THE FOLLOWING ERROR" + vbCrLf + ex.Message, MsgBoxStyle.Critical, "Connection Test")
        End Try

        If CN.State = ConnectionState.Open Then CN.Close()
    End Sub

    Private Function GetTableContent(ByVal CN As SqlConnection) As String
        If CN.State = ConnectionState.Closed Then Return ""

        Dim str As String = ""
        Dim cnt As Integer = 1
        Dim sqlcmd As New SqlCommand("SELECT * FROM Hello", CN)
        Dim reader As SqlDataReader
        reader = sqlcmd.ExecuteReader

        While reader.Read
            str += cnt.ToString + " - " + Convert.ToString(reader.Item("MsgID")) + ", "
            str += Convert.ToString(reader.Item("MsgSubject"))
            str += vbCrLf
            cnt += 1
        End While

        Return str
    End Function

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim CN As New SqlConnection("Data Source = " + server.Text + " ;" + "Initial Catalog = " + "" + "; uid = " + user.Text + ";" + "password = " + pass.Text)
        CN.Open()

        Dim res = GetTableContent(CN)

        CN.Close()
        MsgBox(res)
    End Sub
End Class
