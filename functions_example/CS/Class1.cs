using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.Linq;

namespace functions_example
{
    public static class FunctionLibrary
    {
        [Description("Square sum///sqsum([A:(1,2,3)])")]
        public static decimal sqsum(IEnumerable<decimal> a)
        {
            return a.Sum(x => x * x);
        }

        [Description("Greatest common divisor")]
        public static decimal gcd(decimal x, decimal y)
        {
            ulong a = (ulong)x;
            ulong b = (ulong)y;

            while (a != 0 && b != 0)
            {
                if (a > b)
                    a %= b;
                else
                    b %= a;
            }

            return a | b;
        }

        [Description("Join ranges")]
        public static IEnumerable<decimal> join_seq(IEnumerable<decimal> a, IEnumerable<decimal> b)
        {
            return a.Concat(b);
        }

        [Description("Data source for the PostgreSQL database")]
        public static IEnumerable<string[]> data_source_pg(string connection_string, string select)
        {
            using var conn = new Npgsql.NpgsqlConnection(connection_string);
            conn.Open();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = select;
            var reader = cmd.ExecuteReader();
            var header = reader.GetColumnSchema().Select(x => x.ColumnName).ToArray();
            object[] values = new object[header.Length];

            yield return header;

            while (reader.Read())
            {
                reader.GetValues(values);
                yield return values.Select(x => x is IFormattable f ? f.ToString(null, CultureInfo.InvariantCulture) : x?.ToString()).ToArray();
            }

        }

        [Description("Custom data source which executes a command before the acutal data source is created")]
        public static IEnumerable<string[]> data_source_custom(Func<IEnumerable<string[]>> csv_source) // we use Func<> to execute the data_source_csv_file after the command line command is executed
        {
            Process.Start("cmd.exe", new string[] { "/c", "echo LIST_A_ID,VALUE_02 > text.csv" }).WaitForExit(); // start command line process to generate a CSV
            Process.Start("cmd.exe", new string[] { "/c", $"echo 1,{DateTime.Now.Second} >> text.csv" }).WaitForExit();

            return csv_source(); // now execute the actual CSV data source

            // The following format formula could be used in a model with List A:
            // formatbutton("test", update(import_values('Sheet 1', ext_data_source_custom(data_source_csv_file("text.csv", ",")))))
        }
    }
}