import csv


def create_statistics(chars, lines, value, value_after_loss, value_after_rally, stats_file):

    with open(chars) as f:
        char_amount = f.readline()
    char_amount = int(char_amount)

    with open(lines) as f:
        line_amount = f.readline()
    line_amount = int(line_amount)

    with open(value) as f:
        val = f.readline()
    val = float(val)

    with open(value_after_loss) as f:
        val_loss = f.readline()
    val_loss = float(val_loss)

    with open(value_after_rally) as f:
        val_rally = f.readline()
    val_rally = float(val_rally)

    with open(stats_file, 'w', newline='') as stats:
        writer = csv.writer(stats, delimiter='\t')
        writer.writerow(["Total characters", "Total rows", "Portfolio Value",
                         "Portfolio Value After Loss", "Portfolio Value After Rally in Big Tech"])
        writer.writerow([char_amount, line_amount, val, val_loss, val_rally])
