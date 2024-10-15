
from base64 import b64decode
import logging
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import abi

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.moting_app.moting_app_client import (
        MotingAppClient,
    )

    app_client = MotingAppClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    algokit_utils.ensure_funded(algod_client, algokit_utils.EnsureBalanceParameters(account_to_fund=app_client.app_address, min_spending_balance_micro_algos=1_000_000))

    name = "world"
    response = app_client.hello(name=name)
    logger.info(
        f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
        f"with name={name}, received: {response.return_value}"
    )

    move = 11
    box_name = abi.UintType(64).encode(move)

    response = app_client.make_move(move=move, color="blue", transaction_parameters =  algokit_utils.TransactionParameters(boxes=[(app_client.app_id, box_name)]))
    logger.info(
        f"Called make_move on {app_spec.contract.name} ({app_client.app_id}) "
        f"with move={move}, color=red"
    )

    box_abi = abi.ABIType.from_string("(address,string)")
    box_value = b64decode(algod_client.application_box_by_name(app_client.app_id, box_name)["value"])
    author, color = box_abi.decode(box_value)
    logger.info(f"Box value: author={author}, color={color}")
  
