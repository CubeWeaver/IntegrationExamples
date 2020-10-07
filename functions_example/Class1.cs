using System;
using System.Collections.Generic;
using System.Linq;

namespace functions_example
{
    public static class FunctionLibrary
    {
        public static decimal sqsum(IEnumerable<decimal> a)
        {
            return a.Sum(x => x * x);
        }

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

        public static IEnumerable<decimal> join_seq(IEnumerable<decimal> a, IEnumerable<decimal> b)
        {
            return a.Concat(b);
        }
    }
}
