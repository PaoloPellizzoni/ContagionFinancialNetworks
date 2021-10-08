class Node:
    def __init__(self, ia, il, ea, d):
        self.interbank_asset = ia
        self.interbank_liability = il
        self.external_assets = ea
        self.deposits = d

    def k(self):
        return (self.interbank_asset + self.external_assets - self.interbank_liability - self.deposits)

    interbank_asset = 0
    interbank_liability = 0
    external_assets = 0
    deposits = 0
    failed = False
    failed_pred = 0
