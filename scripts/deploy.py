from brownie import FundMe, MockV3Aggregator, accounts, config, network
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # If we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

        # print(f"The active network is {network.show_active()}")
        # print("Deploying Mocks...")
        # mock_aggregator = MockV3Aggregator.deploy(
        #     18, 2000000000000000000000, {"from": account}
        # )

    # To verify publishing our source code on ether scan we use this code: publish_source: True
    # To make our contract work, verify and deploy on ganach we pass the price feed address
    # to our fundme contract: 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # to see what network are we on (development or live) and based on that do we need verification or not:
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # NOW WE ARE OFFICIALY LIVE NETWORK (OR DEVELOPMENT) AGNOSTIC!
    print(f"Contract deployed at {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
