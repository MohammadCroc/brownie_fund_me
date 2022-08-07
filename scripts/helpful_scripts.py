from brownie import config, network, accounts, MockV3Aggregator
from web3 import Web3

# When we want to run our contract on a mainnet but localy(!) we use forking
# We maid a mainnet-fork network with alchemy.com http address
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
# when our network is development OR ganach-local we want our contract
# to run on our MOCKS and not pulling it out of config eth_usd_price_feed so :
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# Static variables
DECIMALS = 8
STARTING_PRICE = 200000000000


# def get_account():
#     if network.show_active() == "development":
#         return accounts[0]
#     else:
#         return accounts.add(config["wallets"]["from_key"])


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f'The active network is "{network.show_active()}"')
    print("Deploying Mocks...")
    # with this if statement we can say that if there already is a deployed mock contract
    # use that instead of deploying it every time:
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            STARTING_PRICE,
            {"from": get_account()},
        )  # web3.towei(STARTING_PRICE, "ether") supplys the starting value we want wich is 2 * 10 ** 18
    print("Mocks Deployed!")
