from pydantic import BaseModel, Field
from typing import Literal


class Clause(BaseModel):
    clause_type:str = Field(description="e.g termination laibility confidentiality IP,")
    summary:str = Field(description="a short summary of the clause")
    risk_level:str = Literal["low","medium","high"]
    risk_reason :str = Field(description="reason for the risk level")



class ContractAnalysis(BaseModel):
    parties : list[str]
    effective_date: str | None 
    clauses: list[Clause]
    overall_risk : Literal["low","medium","high"] = Field(description="Overall risk level of the contract")
    red_flag: list[str]  


