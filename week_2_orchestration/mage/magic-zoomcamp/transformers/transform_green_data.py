if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from inflection import underscore

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    data = data[(data['passenger_count'] != 0) & (data['trip_distance'] != 0)]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = [underscore(col) for col in data.columns]

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert not ((output['passenger_count'] == 0) | (output['trip_distance'] == 0)).any(), "Some rows still contain 0 in passenger_count or trip_distance"
    assert 'vendor_id' in output.columns, 'There is no vendor_id column'
    assert output is not None, 'The output is undefined'
