import logging
import os
from fastmcp import FastMCP
from cube_client import CubeClient

logging.basicConfig(level=logging.INFO)

CUBE_URL = os.getenv("CUBE_URL", "http://cube:4000/cubejs-api/v1")
CUBE_SECRET = os.getenv("CUBEJS_API_SECRET", "super-secret-change-later")

cube = CubeClient(CUBE_URL, CUBE_SECRET)

mcp = FastMCP(name="hivenet-analytics")


@mcp.tool()
def get_cube_meta():
    """
    Retrieves the complete semantic and data metadata for all available cubes.
    Includes:
    - Technical names and titles
    - Human-readable descriptions
    - Sample values for every dimension (to ensure filters use real data values)
    """
    logging.info("get_cube_meta called: Starting full discovery")
    try:
        meta = cube.get_meta()
    except Exception as e:
        return {"error": f"Failed to connect to Cube: {str(e)}"}
    cubes = []
    for c in meta.get("cubes", []):
        cube_name = c["name"]
        
        # 1. Process Measures
        measures = [
            {
                "name": m["name"],
                "title": m.get("title"),
                "description": m.get("description"),
                "type": m.get("type")
            }
            for m in c.get("measures", [])
        ]
        # 2. Process Dimensions & Discover Sample Values
        dimensions = []
        for d in c.get("dimensions", []):
            dim_info = {
                "name": d["name"],
                "title": d.get("title"),
                "description": d.get("description"),
                "type": d.get("type"),
                "sample_values": []
            }
            # If it's a categorical field (string), fetch actual data values
            if d.get("type") == "string":
                try:
                    # Run a quick query to get unique values for this specific dimension
                    res = cube.run_query({
                        "query": {
                            "dimensions": [d["name"]],
                            "limit": 10
                        }
                    })
                    # Extract the values from the response rows
                    dim_info["sample_values"] = [row.get(d["name"]) for row in res.get("data", [])]
                except Exception as e:
                    logging.warning(f"Could not fetch samples for {d['name']}: {str(e)}")
            dimensions.append(dim_info)
        cubes.append({
            "name": cube_name,
            "title": c.get("title"),
            "description": c.get("description"),
            "measures": measures,
            "dimensions": dimensions,
            "timeDimensions": [
                {"name": d["name"], "title": d.get("title")}
                for d in dimensions if d["type"] == "time"
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
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=3333
    )