import camelot

tables = camelot.read_pdf(
    "time-table.pdf",
    flavor="lattice",
    pages="1",
    copy_text=["v", "h"],
    joint_tol=10,
)

# camelot.plot(tables[0], kind="text", filename="text-graph")
# camelot.plot(tables[0], kind="grid", filename="grid-graph")

# Convert the table to a csv file
tables[0].to_csv("time-table.csv")
# time.sleep(100)
