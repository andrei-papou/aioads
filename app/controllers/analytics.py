from psycopg2 import IntegrityError
from extensions.controllers import BaseController
from data_access.analytics import ClicksQueryFactory as ClicksQF, ViewsQueryFactory as ViewsQF
from exceptions.analytics import PlacementDoesNotExist


class AnalyticsController(BaseController):

    async def register_click(self, placement_id: int):
        query = ClicksQF.create_click(placement_id)

        async with self.db.acquire() as conn:
            try:
                await conn.execute(query)
            except IntegrityError:
                raise PlacementDoesNotExist()

    async def register_view(self, placement_id: int):
        query = ViewsQF.create_view(placement_id)

        async with self.db.acquire() as conn:
            try:
                await conn.execute(query)
            except IntegrityError:
                raise PlacementDoesNotExist()

    async def get_script(self, placement_id: int):
        """
        Something like this:

        <div id='advert'>
                <img src='{banner_image_url}'>
            </div>
            <script>
                (function() {
                    var advWrapper = document.getElementById('advert'),
                        link = advWrapper.getElementsByTagName('img')[0];

                    adWrapper.onload = function() {
                        var xhr = new XMLHttpRequest();

                        request.open('POST', {view_register_url}, true);
                        request.send(null);
                    };

                    link.onclick = function(event) {
                        var xhr = XMLHttpRequest();

                        xhr.onload = function() {
                            window.location.href = {follow_url_link};
                        };

                        request.open('POST', {click_register_url}, true);
                        request.send(null);

                        event.preventDefault();
                    };
                })();
            </script>
        """
        pass
