#!/usr/bin/env python3

import argparse
import json
import sys

def dump_json(obj, out, pretty):
    if pretty:
        json.dump(obj, out, indent=2, sort_keys=True)
    else:
        json.dump(obj, out, separators=(",", ":"), sort_keys=True)
    return

def main():
    parser = argparse.ArgumentParser(description="Change an asset's symbol with referential integrity")
    parser.add_argument("-o", "--output", metavar="OUT", default="-", help="output filename (default: stdout)")
    parser.add_argument("-i", "--input", metavar="IN", default="-", help="input filename (default: stdin)")
    parser.add_argument("-f", "--from", metavar="PREFIX", default="", help="initial prefix")
    parser.add_argument("-t", "--to", metavar="PREFIX", default="", help="new prefix")
    parser.add_argument("-p", "--pretty", action="store_true", default=False, help="pretty print output")
    opts = parser.parse_args()

    if opts.input == "-":
        genesis = json.load(sys.stdin)
    else:
        with open(opts.input, "r") as f:
            genesis = json.load(f)

    frum = opts.__dict__["from"]    # from is a language keyword and cannot be an attribute name

    for asset in genesis["initial_assets"]:
        if asset["symbol"] == frum:
            asset["symbol"] = opts.to

    for balance in genesis["initial_balances"]:
        if balance["asset_symbol"] == frum:
            balance["asset_symbol"] = opts.to

    for vb in genesis["initial_vesting_balances"]:
        if balance["asset_symbol"] == frum:
            balance["asset_symbol"] = opts.to

    if opts.output == "-":
        dump_json( genesis, sys.stdout, opts.pretty )
        sys.stdout.flush()
    else:
        with open(opts.output, "w") as f:
            dump_json( genesis, f, opts.pretty )
    return

if __name__ == "__main__":
    main()
