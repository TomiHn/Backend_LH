from routers import route_get, route_post, route_delete


from fastapi import FastAPI

app = FastAPI(title="AnturiAPI", description="Loppuharkan anturi api")

app.include_router(route_get.router_gets, tags=["Get methods"])
app.include_router(route_post.router_posts, tags=["Post methods"])
app.include_router(route_delete.router_deletes, tags=["Delete methods"])