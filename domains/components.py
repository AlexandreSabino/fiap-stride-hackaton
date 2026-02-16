
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Component(BaseModel):
    id: str = Field(..., description="Unique identifier (e.g., 'alb_a')")
    name: str = Field(..., description="Exact label found in the diagram (e.g., 'SEI / SIP')")
    type: str = Field(..., description="Specific technology (e.g., 'EC2', 'RDS')")
    category: str = Field(..., description="Compute, Database, Network, Security, etc.")
    parent_id: Optional[str] = Field(None, description="ID of the container/zone this component is inside")
    trust_zone: str = Field(..., description="Public, Private, DMZ, or AWS")
    notes: Optional[str] = Field(None, description="Extra context like 'Primary' or 'Zone A'")
    is_managed_service: bool = Field(...,description="True se for um serviço gerenciado (S3, Lambda) e False se for IaaS (EC2)")
    data_sensitivity: str = Field("Unknown", description="Level of data sensitivity (PII, Financial, Public)")
    internet_exposed: bool = Field(..., description="Is this component directly reachable from the internet?")
    authentication: Optional[str] = Field(None, description="Type of auth visible (IAM, API Key, None)")

class Flow(BaseModel):
    id: str
    source_id: str
    target_id: str
    interaction_type: str = Field(..., description="Protocol or interaction (HTTPS, SQL, etc.)")
    direction: str = Field(..., description="Uni-directional or Bi-directional")

class ArchitectureAnalysis(BaseModel):
    components: List[Component]
    flows: List[Flow]
    trust_boundaries: List[str] = Field(default_factory=list)