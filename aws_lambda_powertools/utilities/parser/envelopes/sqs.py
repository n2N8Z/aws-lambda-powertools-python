import logging
from typing import Any, Dict, List, Union

from pydantic import BaseModel

from ..schemas import SqsSchema
from .base import BaseEnvelope

logger = logging.getLogger(__name__)


class SqsEnvelope(BaseEnvelope):
    """SQS Envelope to extract array of Records

    The record's body parameter is a string, though it can also be a JSON encoded string.
    Regardless of it's type it'll be parsed into a BaseModel object.

    Note: Records will be parsed the same way so if schema is str,
    all items in the list will be parsed as str and npt as JSON (and vice versa)
    """

    def parse(self, data: Dict[str, Any], schema: Union[BaseModel, str]) -> List[Union[BaseModel, str]]:
        """Parses records found with schema provided

        Parameters
        ----------
        data : Dict
            Lambda event to be parsed
        schema : BaseModel
            User schema provided to parse after extracting data using envelope

        Returns
        -------
        List
            List of records parsed with schema provided
        """
        parsed_envelope = SqsSchema(**data)
        output = []
        for record in parsed_envelope.Records:
            output.append(self._parse(record.body, schema))
        return output
