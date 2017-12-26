{{Testy}}

{{#each Client}}
select *
from {{LoaderDatabase}}..data_Claimline

{{/each}}
{{#each Boomer}}
select *
from {{LoaderDatabase}}..data_Claimline

{{/each}}
--HOW SEXY (and simple) IS THIS????
