# --> Import required modules
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from Pages.database_engine import ClientDatabase

# --> Initialize clients database
clients = ClientDatabase()


class PdfEngine:
    @classmethod
    def generate_clients_list(cls):
        # --> Create Document
        doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)

        # --> container for the 'Flowable' objects
        elements = []

        # --> Get all clients from database
        data = clients.get_all_clients()

        data.insert(0, ["Firstname", "Lastname", "Phone", "Email", "Home Address"])
        table_title = Table([["List of clients"]])
        t = Table(data, colWidths=[100, 100, 60, 100, 160])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                               ("FONT", (0, 0), (-1, 0), "Helvetica", 10), ("FONT", (0, 0), (-1, -1), "Helvetica", 7),
                               ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey)]))
        elements.append(table_title)
        elements.append(t)
        # write the document to disk
        doc.build(elements)

