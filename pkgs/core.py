#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import json
import os
import re

date = re.compile(r"(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])")


def authorship(author, title, year, month, day):  # {{{
    Month = {
        "01": "janeiro",
        "02": "fevereiro",
        "03": "março",
        "04": "abril",
        "05": "maio",
        "06": "junho",
        "07": "julho",
        "08": "agosto",
        "09": "setembro",
        "10": "outubro",
        "11": "novembro",
        "12": "dezembro",
    }
    acmd = r"\seminar{%s}{%s}{%s}{%s}{%s}" % (
        author,
        title,
        year,
        Month[month],
        day,
    )
    with open("auth.tex", "w") as afile:
        print(acmd, file=afile)  # }}}


def genpdf(author, title, year, month, day):  # {{{
    os.system("xelatex main && xelatex main")
    pdfname = "cert_{year}_{month}_{day}.pdf".format(
        year=year,
        month=month,
        day=day,
    )
    os.system(r"mv main.pdf pdf/{pdfname}".format(pdfname=pdfname))
    return pdfname  # }}}


def sendmail(author, address, title, year, month, day, cert):  # {{{
    body = r"""
    Olá, {author}!

    Eis aqui o certificado do seu seminário de geometria, intitulado

      {title},

    o qual foi ministrado em {day} de {month} de {year}.

    Agradecemos imensamente pela participação.

    Atenciosamente,
    Hiuri Reis
    """.format(
        author=author, title=title, year=year, month=month, day=day
    )
    with open("mail.txt", "w") as f:
        print(body, file=f)
    subject = r"certificado de apresentação do seu seminário de geometria"
    sendcmd = r"mutt -s '{subject}' -a {file} -- {email} < mail.txt".format(
        subject=subject, file=cert, email=address
    )
    os.system(sendcmd)  # }}}


def main():
    with open("pkgs/data.json", "r") as raw_json_file:
        json_file = json.load(raw_json_file)
        for talk in json_file:
            d = date.match(talk["date"])
            Y = d.group(1)
            M = d.group(2)
            D = d.group(3)
            authorship(talk["author"], talk["title"], Y, M, D)
            genpdf(talk["author"], talk["title"], Y, M, D)
            # sendmail(
            #     talk["author"],
            #     talk["email"],
            #     talk["title"],
            #     Y,
            #     M,
            #     D,
            #     cert,
            # )


if __name__ == "__main__":
    main()
