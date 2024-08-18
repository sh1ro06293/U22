$('.flexdatalist').flexdatalist({
    minLength: 1,
    searchIn: 'name',
    data: "{{ url_for('static', filename='json/stationData.json') }}",
    selectionRequired: true,
});
