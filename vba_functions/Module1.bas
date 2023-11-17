Public cw_dirty As Boolean

Function cw_cell(url As String, cube As String, ParamArray coords() As Variant) As Variant
    Application.Volatile
    
    Dim i As Integer
    
    url = url & "cell/" & WorksheetFunction.EncodeURL(cube) & "/"
    
    For i = LBound(coords) To UBound(coords)
        url = url & WorksheetFunction.EncodeURL(coords(i) & ";")
    Next i
    
    cw_cell = Val(cw_web_call(url))
End Function

Function cw_update_cell_if(condition As Boolean, value As Variant, url As String, cube As String, ParamArray coords() As Variant) As Variant
    If condition Then
        Dim tempCoords As Variant
        tempCoords = coords
        cw_update_cell_if = cw_update_cell_internal(value, url, cube, tempCoords)
    Else
        cw_update_cell_if = ""
    End If
End Function

Function cw_update_cell(value As Variant, url As String, cube As String, ParamArray coords() As Variant) As Variant
    Dim tempCoords As Variant
    tempCoords = coords
    cw_update_cell = cw_update_cell_internal(value, url, cube, tempCoords)
End Function

Private Function cw_update_cell_internal(value As Variant, url As String, cube As String, coords As Variant) As Variant
    If value = "" Then
        value = "0"
    End If
    
    Dim i As Integer
    
    url = url & "update_cell/" & WorksheetFunction.EncodeURL(Str(value)) & "/" & WorksheetFunction.EncodeURL(cube) & "/"
    
    For i = LBound(coords) To UBound(coords)
        url = url & WorksheetFunction.EncodeURL(coords(i) & ";")
    Next i
    
    Dim resp As String
    resp = cw_web_call(url)
    
    cw_update_cell_internal = Val(Mid(resp, 2))
    If Left(resp, 1) = "1" Then
        cw_dirty = True
    End If
    
End Function

Private Function cw_web_call(url As String) As String
    Dim xmlHttp As Object
    Set xmlHttp = CreateObject("MSXML2.ServerXMLHTTP.6.0")

    xmlHttp.Open "GET", url, False
    xmlHttp.send
    
    If Err.Number <> 0 Then
        cw_web_call = "Error: " & Err.Description
        Exit Function
    End If

    If xmlHttp.Status = 200 Then
        cw_web_call = xmlHttp.responseText
    Else
        cw_web_call = "Error: HTTP request failed with status code " & xmlHttp.Status
    End If

    Set xmlHttp = Nothing
End Function

Function cw_list(url As String, list As String, Optional parent As String)
    Dim xmlHttp As Object
    Dim htmlDoc As Object
    Dim table As Object
    Dim row As Object
    Dim cell As Object
    Dim tableData As Variant
    Dim i As Integer
    Dim j As Integer

    Set xmlHttp = CreateObject("MSXML2.ServerXMLHTTP")
    Set htmlDoc = CreateObject("htmlfile")
    
    url = url & "list/" & WorksheetFunction.EncodeURL(list)
    If Not IsMissing(parent) Then
        url = url & "/" & WorksheetFunction.EncodeURL(parent)
    End If

    xmlHttp.Open "GET", url, False
    xmlHttp.send

    htmlDoc.body.innerHTML = xmlHttp.responseText

    Set table = htmlDoc.getElementsByTagName("table")(0)

    If Not table Is Nothing Then
        Dim numRows As Integer
        Dim numCols As Integer
        numRows = table.Rows.Length
        numCols = table.Rows(1).Cells.Length

        ReDim tableData(1 To numRows, 1 To numCols)

        For i = 1 To numRows
            Set row = table.Rows(i - 1)
            For j = 1 To numCols
                Set cell = row.Cells(j - 1)
                tableData(i, j) = cell.innerText
            Next j
        Next i

        cw_list = tableData
    Else
        cw_list = "No table found in the HTML content."
    End If
End Function


