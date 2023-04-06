db.subscribers.aggregate( [
    {$match: { inUse: null}},
    {$project: {"slice.session.name": 1}},
    {$unwind: {path: "$slice"}},
    {$addFields: { name: { $arrayElemAt: [ "$slice.session.name", 0 ] } }},
    {$project: {"name": 1}},
    {$group: {_id: "$name", count: {$sum: 1}}},
    {$match: { _id: {$ne: "internet"}}},
    {$sort: {"count": -1}},
    {$limit: 1}
 ] ).forEach(function(obj){
    slice = obj._id;
});
ret = db.subscribers.findAndModify( {
        query: {"slice.session.name": slice, "inUse": null},
        update: { $set:{"inUse": 1}} ,
        fields: {"imsi": 1},
        new: true
    });
if( ret != null)
    print(ret.imsi);
