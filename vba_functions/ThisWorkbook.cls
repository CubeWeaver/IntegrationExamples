Dim oldFormula As String
Dim oldRange As String
Private Sub Workbook_SheetSelectionChange(ByVal Sh As Object, ByVal Target As Excel.Range)
    If Target.Count = 1 Then
        oldRange = Target.Address
        oldFormula = Target.Formula
    Else
        oldRange = ""
    End If
    
End Sub

Private Sub Workbook_SheetChange(ByVal Sh As Object, ByVal Target As Range)
    
    If (oldRange = Target.Address) And (Left(oldFormula, Len("=CW_CELL(")) = "=CW_CELL(") And (IsNumeric(Target.Formula)) Then
        Evaluate ("=cw_update_cell(" & Target.Formula & "," & Mid(oldFormula, Len("=CW_CELL(") + 1))
        Application.EnableEvents = False
        Application.Undo
        Application.EnableEvents = True
    End If
End Sub

Private Sub Workbook_SheetCalculate(ByVal Sh As Object)
    If Module1.cw_dirty Then
       Module1.cw_dirty = False
       Application.Calculate
    End If
End Sub

