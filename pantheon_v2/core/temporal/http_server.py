from fastapi import FastAPI, status, Body
from zamp_public_workflow_sdk.temporal.temporal_service import TemporalService
from pantheon_v2.core.temporal.workers import TemporalWorkerManager
from zamp_public_workflow_sdk.temporal.temporal_client import RunWorkflowParams

app = FastAPI()


@app.post("/workflow", status_code=status.HTTP_200_OK)
async def start_workflow(params: dict = Body(...)):
    manager = TemporalWorkerManager()
    service: TemporalService = await TemporalService.connect(manager.client_config)
    workflow_params = RunWorkflowParams(**params)
    await service.start_async_workflow(workflow_params)
    return {"message": "Workflow started successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9233)
