import  yaml
from validator import validate
from datadog_api_client.v2.model.service_definition_v2_dot2 import ServiceDefinitionV2Dot2
from datadog_api_client.v2.model.service_definition_v2_dot2_version import ServiceDefinitionV2Dot2Version
from datadog_api_client.v2.model.service_definition_v2_dot2_link import ServiceDefinitionV2Dot2Link
from datadog_api_client.model_utils import change_keys_js_to_python




# This function will convert an opslevel service to a datadog service
def convert(OpsLevelFile) -> str|None:
    # Load the yaml file
    with open(OpsLevelFile, 'r') as file:
        OpsLevelService = yaml.safe_load(file)

    dataDogService = ServiceDefinitionV2Dot2(
        schema_version = ServiceDefinitionV2Dot2Version.V2_2,
        dd_service = "",
        links = []
    )

    # Check if service is present
    if "service" in OpsLevelService:
        service = OpsLevelService["service"]
        dataDogService.dd_service = service["name"]
        dataDogService.team = service.get("owner", "")
        dataDogService.application = service.get("system", "")
        dataDogService.description = service.get("description", "")
        dataDogService.tier = service.get("tier", "")
        dataDogService.lifecycle = service.get("lifecycle", "")

        if service.get("language"):
            dataDogService.languages = [service["language"]]

        if service.get("tags"):
            dataDogService.tags = service["tags"]

        if service.get("repositories"):
            for repo in service["repositories"]:
                dataDogService.links.append(
                    ServiceDefinitionV2Dot2Link(
                        name=repo["name"],
                        type="repo",
                        url=f"https://{repo['provider']}.com/{repo['name']}",
                        provider=repo["provider"].capitalize()
                    )
                )

        if service.get("tools"):
            for tool in service["tools"]:
                dataDogService.links.append(
                    ServiceDefinitionV2Dot2Link(
                        name=tool["name"],
                        type=tool["category"],
                        url=tool["url"]
                    )
                )

    # Check if repository is present instead of service TODO: Check if we want this
    elif "repository" in OpsLevelService:
        repository = OpsLevelService["repository"]
        dataDogService.dd_service = repository["name"]
        dataDogService.team = repository.get("owner", "")

    # If neither service nor repository is present, return None
    else:
        return None
        
    
    # Validate the data dog service
    dataDogService = change_keys_js_to_python(dataDogService.attribute_map, dataDogService)
    print(dataDogService)
    # if not validate(dataDogService.attribute_map, dataDogService):
    #     return None
    
    # return yaml.dump(dataDogService)
    return None

