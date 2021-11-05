Imports System.ComponentModel
Public NotInheritable Class FunctionLibrary

    <Description("Square sum///sqsum([A:(1,2,3)])")>
    Public Shared Function sqsum(a As IEnumerable(Of Decimal)) As Decimal
        Return a.Sum(Function(x) x * x)
    End Function

    <Description("Greatest common divisor")>
    Public Shared Function gcd(x As Decimal, y As Decimal) As Decimal
        Dim a As ULong = Convert.ToUInt64(x)
        Dim b As ULong = Convert.ToUInt64(y)

        Do While (a <> 0 And b <> 0)
            If a > b Then
                a = a Mod b
            Else
                b = b Mod a
            End If
        Loop

        Return a Or b
    End Function

    <Description("Join ranges")>
    Public Shared Function join_seq(a As IEnumerable(Of Decimal), b As IEnumerable(Of Decimal)) As IEnumerable(Of Decimal)
        Return a.Concat(b)
    End Function
End Class
