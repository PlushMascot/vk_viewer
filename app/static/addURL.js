function addURL(element)
{
    $(element).attr('href', function() {
        return this.href +
        `?id=${this.id}` +
        `&order=${$("#select_order_filter").val()}` +
        `&start=${$("#date_range").text().split(' - ')[0]}` +
        `&end=${$("#date_range").text().split(' - ')[1]}`;
    });
}