import logging
from fastmcp import FastMCP
from cube_client import CubeClient

logging.basicConfig(level=logging.INFO)

CUBE_URL = "http://cube:4000/cubejs-api/v1"
cube = CubeClient(CUBE_URL)

mcp = FastMCP(name="hivenet-analytics")


@mcp.tool()
def get_cube_meta():
    logging.info("get_cube_meta called")

    meta = cube.get_meta()

    cubes = []
    for c in meta.get("cubes", []):
        cubes.append({
            "name": c["name"],
            "measures": [m["name"] for m in c.get("measures", [])],
            "dimensions": [d["name"] for d in c.get("dimensions", [])],
            "timeDimensions": [
                d["name"]
                for d in c.get("dimensions", [])
                if d.get("type") == "time"
            ],
        })

    return {"cubes": cubes}


@mcp.tool()
def run_cube_query(
    measures: list[str],
    dimensions: list[str] | None = None,
    time_dimension: str | None = None,
    date_range: list[str] | None = None,
    limit: int | None = None,
):
    logging.info(
        "run_cube_query called | measures=%s dimensions=%s time_dimension=%s date_range=%s limit=%s",
        measures,
        dimensions,
        time_dimension,
        date_range,
        limit,
    )

    query = {
        "measures": measures,
        "dimensions": dimensions or [],
    }

    if time_dimension and date_range:
        query["timeDimensions"] = [
            {
                "dimension": time_dimension,
                "dateRange": date_range,
            }
        ]

    if limit:
        query["limit"] = limit

    result = cube.run_query({"query": query})
    return result.get("data", [])


if __name__ == "__main__":
    print("🚀 hivenet-analytics MCP ready", flush=True)
    if __name__ == "__main__":
        mcp.run(
        transport="http",
        host="0.0.0.0",
        port=3333
        )
